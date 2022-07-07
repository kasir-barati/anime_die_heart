import os
import math
from celery import shared_task
from ..utils.resize_video import resize_video


@shared_task
def celery_resize_file(
        original_video_abs_path: str,
        resized_file_abs_path: str,
        size_divided_by: int) -> None:
    video_size = os.path.getsize(
        original_video_abs_path,
    )
    file_size = math.ceil(video_size/size_divided_by)

    resize_video(
        video_absolute_path=original_video_abs_path,
        output_file_absolute_path=resized_file_abs_path,
        size_upper_bound=file_size,
    )

