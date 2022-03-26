from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get_unread_info(self, convo_dict, user_id, user_last_read, other_last_read):
        try:
            looking_for_last_unread = True
            looking_for_unread_count = True
            unread_count = 0
            for message in reversed(convo_dict["messages"]):

                if not looking_for_last_unread and not looking_for_unread_count:
                    return

                if user_last_read:    
                    if looking_for_unread_count and self.isUnread(message, user_id, user_last_read):
                        unread_count += 1
                    else:
                        convo_dict["unreadCount"] = unread_count
                        looking_for_unread_count = False
                else:
                    unread_count += 1
                    convo_dict["unreadCount"] = unread_count

                if other_last_read:
                    has_read = self.hasOtherRead(message, user_id, other_last_read)
                    if looking_for_last_unread and has_read:
                        message["isLastReadByOther"] = True
                        looking_for_last_unread = False
                        
        except Exception as e:
            print(e)
    
    def isUnread(self, message, user_id, user_last_read):
        if message["senderId"] != user_id:
            created_at = message["createdAt"]
            created_is_newer = user_last_read <= created_at
            return created_is_newer
    
    def hasOtherRead(self, message, user_id, other_last_read):
        if  message["senderId"] == user_id:
            created_at = message["createdAt"]
            last_read_is_newer = created_at <= other_last_read
            return last_read_is_newer
    
    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                .all()
            )

            conversations_response = []

            for convo in conversations:
                convo_dict = {
                    "id": convo.id,
                    "messages": [
                        message.to_dict(["id", "text", "senderId", "createdAt"])
                        for message in convo.messages.all()
                    ],
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]

                # set a property "otherUser" so that frontend will have easier access
                # get all unread data which is then added within the get function
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                    user_last_read = convo.user2ReadReceipt
                    other_last_read = convo.user1ReadReceipt
                    self.get_unread_info(convo_dict, user_id, user_last_read, other_last_read)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)
                    user_last_read = convo.user1ReadReceipt
                    other_last_read = convo.user2ReadReceipt
                    self.get_unread_info(convo_dict, user_id, user_last_read, other_last_read)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                conversations_response.append(convo_dict)
            conversations_response.sort(
                key=lambda convo: convo["messages"][-1]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)
