from app.async_tasks import establish


def start_sending_email(email):
    establish.logger.info('STARTING SENDING EMAIL')
    task = send_email.apply_async((email, ))
    return task.id


@establish.worker.task
def send_email(email):
    for number in range(1, 100000):
        print(email + str(number))
