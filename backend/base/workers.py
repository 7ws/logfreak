from django_rq import job


@job('default')
def get_new_data(source):
    """Wrapper function to enqueue `source.get_new_data`
    """
    source.get_new_data()
