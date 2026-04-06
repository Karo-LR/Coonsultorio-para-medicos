from django.forms.models import model_to_dict

from core.models import AuditLog


def _actor_from_request(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return user
    return None


def _resource_payload(instance):
    if instance is None:
        return {
            "resource_type": "system",
            "resource_id": "",
            "resource_repr": "",
        }

    return {
        "resource_type": instance._meta.label_lower,
        "resource_id": str(instance.pk),
        "resource_repr": str(instance)[:255],
    }


def _request_metadata(request):
    if request is None:
        return {}

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.META.get("REMOTE_ADDR", "")
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    return {
        "ip_address": ip_address,
        "user_agent": user_agent[:255],
    }


def log_event(request, action, instance=None, description="", metadata=None):
    payload = _resource_payload(instance)
    extra_metadata = metadata.copy() if metadata else {}
    extra_metadata.update(_request_metadata(request))

    AuditLog.objects.create(
        actor=_actor_from_request(request),
        action=action,
        resource_type=payload["resource_type"],
        resource_id=payload["resource_id"],
        resource_repr=payload["resource_repr"],
        description=description[:255],
        metadata=extra_metadata,
    )


def snapshot_instance(instance, fields=None):
    if instance is None:
        return {}

    data = model_to_dict(instance, fields=fields)
    return {key: str(value) for key, value in data.items()}
