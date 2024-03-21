from rest_framework import filters


class IsOwnerOfOrder(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset

        return queryset.filter(user_id=request.user.id)
