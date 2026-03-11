import json
from django.contrib.auth import get_user_model
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage

User = get_user_model()


def room_name_for(u1_id, u2_id):
    a, b = sorted([u1_id, u2_id])
    return f"dm_{a}_{b}"


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.other_user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
        self.other_user = await self.get_user(self.other_user_id)
        if not self.other_user:
            await self.close()
            return

        self.room_group_name = room_name_for(user.id, self.other_user_id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Mark unread messages from other_user -> me as read
        unread_ids = await self.mark_unread_as_read(reader_id=user.id, sender_id=self.other_user_id)
        if unread_ids:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "read_receipt_event",
                "message_ids": unread_ids,
                "reader_id": user.id,
            })

        await self.set_presence(user.id, True)

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if not user.is_anonymous:
            await self.set_presence(user.id, False)

        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = self.scope["user"]
        if user.is_anonymous:
            return

        data = json.loads(text_data)
        msg = (data.get("message") or "").strip()
        temp_id = data.get("temp_id")  # for optimistic UI

        if not msg:
            return

        message = await self.create_message(user.id, self.other_user_id, msg)

        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message_event",
            "temp_id": temp_id,
            "message_id": message["id"],
            "message": message["content"],
            "sender_id": message["sender_id"],
            "receiver_id": message["receiver_id"],
            "created_at": message["created_at"],
        })

    async def chat_message_event(self, event):
        # Send message to browser
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "temp_id": event.get("temp_id"),
            "message_id": event["message_id"],
            "message": event["message"],
            "sender_id": event["sender_id"],
            "receiver_id": event["receiver_id"],
            "created_at": event["created_at"],
        }))

        # If I'm the receiver and I'm currently in this chat, mark read & broadcast ✓✓
        user = self.scope["user"]
        if user.is_anonymous:
            return

        if user.id == event["receiver_id"]:
            updated = await self.mark_specific_as_read(user.id, event["message_id"])
            if updated:
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "read_receipt_event",
                    "message_ids": [event["message_id"]],
                    "reader_id": user.id,
                })

    async def read_receipt_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "read_receipt",
            "message_ids": event["message_ids"],
            "reader_id": event["reader_id"],
        }))

    # ---------- DB helpers ----------
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, sender_id, receiver_id, content):
        m = ChatMessage.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        return {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
        }

    @database_sync_to_async
    def mark_unread_as_read(self, reader_id, sender_id):
        qs = ChatMessage.objects.filter(
            sender_id=sender_id,
            receiver_id=reader_id,
            is_read=False
        )
        ids = list(qs.values_list("id", flat=True))
        if ids:
            qs.update(is_read=True, read_at=timezone.now())
        return ids

    @database_sync_to_async
    def mark_specific_as_read(self, reader_id, message_id):
        updated = ChatMessage.objects.filter(
            id=message_id,
            receiver_id=reader_id,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return updated > 0

    @database_sync_to_async
    def set_presence(self, user_id, online: bool):
        User.objects.filter(id=user_id).update(
            is_online=online,
            last_seen=timezone.now()
        )