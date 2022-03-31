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

            conversation = None
            queried_convo = None

            if conversation_id:
                conversation = Conversation.objects.filter(id=conversation_id)
                queried_convo = conversation.first()
                
                if not queried_convo:
                    return HttpResponse(status=204)
                if queried_convo.user1.id != sender_id and queried_convo.user2.id != sender_id:
                    return HttpResponse(status=401)

                if sender_id == queried_convo.user1.id:
                    conversation.update(user1ReadReceipt=timezone.now())
                    return HttpResponse(status=200)
                elif sender_id == queried_convo.user2.id:
                    conversation.update(user2ReadReceipt=timezone.now())
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=204)
            return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(status=500)