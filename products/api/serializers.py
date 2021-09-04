from rest_framework import serializers
from products.models import Item, Category


class ProductCreationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}

    def get_price(self, instance):
        # item will be sent to calculate_price function in Item model to return item best price
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        # item will be sent to calculate_price function in Item model to return item availability
        return instance.get_is_available(instance.branchitem_set.all())

    def get_categories(self, instance):
        # return item category title
        categories = instance.categories.values('title')
        if categories:
            return categories
        return None

    def get_branch(self, instance):
        # return item branch
        return instance.get_best_branch(instance.branchitem_set.all())


class ProductBranchItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}

    def get_price(self, instance):
        # item will be sent to calculate_price function in Item model to return item best price
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        # item will be sent to calculate_price function in Item model to return item availability
        return instance.get_is_available(instance.branchitem_set.all())

    def get_categories(self, instance):
        # return item category title
        categories = instance.categories.values('title')
        if categories:
            return categories
        return None

    def get_branch(self, instance):
        # return item branch
        return instance.get_best_price_branch(instance.branchitem_set.all())


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
