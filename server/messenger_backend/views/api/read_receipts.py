from django.contrib.auth.middleware import get_user
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from rest_framework.views import APIView

class ReadReceipt(APIView):
    "Sets read receipt for users. Expects { conversationId }"

    def post(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            sender_id = user.id
            body = request.data
            conversation_id = body.get("conversationId")

            if conversation_id:
                conversation = Conversation.objects.filter(id=conversation_id).first()
                if sender_id == conversation.user1.id:
                    conversation.user1ReadReceipt = timezone.now()
                elif sender_id == conversation.user2.id:
                    conversation.user2ReadReceipt = timezone.now()
                conversation.save()
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)