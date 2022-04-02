from telnetlib import STATUS
from django.db.models import Q
from django.db.models.query import Prefetch
from django.contrib.auth.middleware import get_user
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from rest_framework.views import APIView

class ReadReceipt(APIView):
    "Sets read receipt for users. Expects { conversationId }"

    def patch(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            sender_id = user.id
            body = request.data
            conversation_id = body.get("conversationId")

            if conversation_id:
                conversation = Conversation.objects.filter(id=conversation_id).prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                queried_convo = conversation.first()
                
                if not queried_convo:
                    return HttpResponse(status=204)
                if queried_convo.user1.id != sender_id and queried_convo.user2.id != sender_id:
                    return HttpResponse(status=401)
                elif queried_convo.user1.id == sender_id or queried_convo.user2.id == sender_id:
                    queried_convo.messages.all().filter(~Q(senderId=sender_id), isReadByOther=False).update(isReadByOther=True)
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=204)
            return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(status=500)