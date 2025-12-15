from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import ServiceCategory, ProductExample, CustomerInquiry, QuoteRequest, PricingTier, SiteConfiguration, SocialMediaLink, CarouselImage


class ProductExampleInline(TabularInline):
    model = ProductExample
    extra = 0
    fields = ['title', 'starting_price', 'is_featured', 'is_active']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ['name', 'icon_preview', 'order', 'product_count', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ProductExampleInline]

    def icon_preview(self, obj):
        return format_html('<i data-feather="{}"></i> {}', obj.icon_class, obj.icon_class)
    icon_preview.short_description = 'Icon'

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(ProductExample)
class ProductExampleAdmin(ModelAdmin):
    list_display = ['title', 'category', 'starting_price', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'description']


class QuoteRequestInline(StackedInline):
    model = QuoteRequest
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomerInquiry)
class CustomerInquiryAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'email', 'service_needed', 'status', 'submitted_on', 'whatsapp_action']
    list_display_links = ['name', 'phone', 'email', 'service_needed', 'submitted_on']
    list_filter = ['status', 'service_needed', 'submitted_on']
    search_fields = ['name', 'email', 'phone', 'company', 'message']
    readonly_fields = ['submitted_on', 'whatsapp_link_display']
    list_editable = ['status']
    date_hierarchy = 'submitted_on'
    inlines = [QuoteRequestInline]

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'phone', 'email', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('service_needed', 'message', 'status')
        }),
        ('Quick Actions', {
            'fields': ('whatsapp_link_display', 'submitted_on'),
            'classes': ('collapse',)
        }),
    )

    def whatsapp_action(self, obj):
        return format_html(
            '<a href="{}" target="_blank" class="text-green-600 hover:text-green-800 font-bold flex items-center gap-1">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16">'
            '<path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>'
            '</svg>'
            ' WhatsApp</a>',
            obj.whatsapp_link
        )
    whatsapp_action.short_description = 'Follow Up'

    def whatsapp_link_display(self, obj):
        return format_html(
            '<a href="{}" target="_blank" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors flex items-center gap-2 w-fit">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16">'
            '<path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>'
            '</svg>'
            ' Open WhatsApp Chat</a>',
            obj.whatsapp_link
        )
    whatsapp_link_display.short_description = 'WhatsApp Link'


@admin.register(QuoteRequest)
class QuoteRequestAdmin(ModelAdmin):
    list_display = ['inquiry', 'estimated_price', 'follow_up_date', 'created_at']
    list_display_links = ['inquiry', 'estimated_price', 'follow_up_date', 'created_at']
    list_filter = ['follow_up_date', 'created_at']
    search_fields = ['inquiry__name', 'inquiry__email', 'notes']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PricingTier)
class PricingTierAdmin(ModelAdmin):
    list_display = ['min_quantity', 'discount_percentage', 'is_active']
    list_editable = ['discount_percentage', 'is_active']
    ordering = ['min_quantity']


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(ModelAdmin):
    list_display = ['site_name', 'phone_contact', 'email_contact']
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the configuration
        return False


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(ModelAdmin):
    list_display = ['name', 'url', 'icon_class', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(CarouselImage)
class CarouselImageAdmin(ModelAdmin):
    list_display = ['title_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']

    def title_preview(self, obj):
        if obj.image:
           return format_html('<img src="{}" style="height: 50px; border-radius: 4px;" /> {}', obj.image.url, obj.title)
        return obj.title
    title_preview.short_description = "Slide"



# Re-register User and Group to use Unfold
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

