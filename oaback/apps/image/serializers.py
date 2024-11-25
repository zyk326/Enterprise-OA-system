from rest_framework import serializers
from django.core.validators import FileExtensionValidator, get_available_image_extensions


class UploadImageSerializer(serializers.Serializer):
    # 校验文件是否是图片

    image = serializers.ImageField(
        # validators=[FileExtensionValidator(get_available_image_extensions())]
        validators = [FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        error_messages = {'required': '请上传图片!', 'invalid_image':'请上传正确格式的图片!'}
    )


    def validate_image(self, value):
        # 图片单位是字节
        # 1024B:1KB
        # 1024KB:1MB
        max_size = 0.5 * 1024 * 1024
        size = value.size
        if size > max_size:
            raise serializers.ValidationError('图片最大不能超过0.5MB!')
        return value