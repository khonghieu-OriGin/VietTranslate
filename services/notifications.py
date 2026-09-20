def should_notify(user, notification_type):
    pref = getattr(user, 'preference', None)

    if not pref:
        return True

    mapping = {
        'JOB_MATCH': 'notify_new_jobs',
        'NEW_MESSAGE': 'notify_messages',
        'CONTRACT_CREATED': 'notify_contracts',
        'NEW_REVIEW': 'notify_reviews',
    }

    field = mapping.get(notification_type)

    if not field:
        return True

    return bool(getattr(pref, field, True))
