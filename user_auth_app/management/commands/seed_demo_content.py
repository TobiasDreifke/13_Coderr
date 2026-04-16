from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review
from user_auth_app.models import UserProfile


DEMO_USERS = [
    {
        "username": "andrey",
        "password": "asdasd",
        "email": "andrey@example.com",
        "first_name": "Andrey",
        "last_name": "Keller",
        "profile": {
            "type": "customer",
            "description": "Ich suche schnelle und saubere Hilfe fuer Webprojekte.",
        },
    },
    {
        "username": "kevin",
        "password": "asdasd24",
        "email": "kevin@example.com",
        "first_name": "Kevin",
        "last_name": "Brandt",
        "profile": {
            "type": "business",
            "location": "Berlin",
            "tel": "+49 30 555 0199",
            "working_hours": "Mo-Fr 09:00-17:00",
            "description": "Full-stack Entwickler fuer Landingpages, APIs und Dashboards.",
        },
    },
    {
        "username": "lara_design",
        "password": "demo12345",
        "email": "lara@example.com",
        "first_name": "Lara",
        "last_name": "Neumann",
        "profile": {
            "type": "business",
            "location": "Hamburg",
            "tel": "+49 40 555 0142",
            "working_hours": "Mo-Do 10:00-18:00",
            "description": "UI und Brand Designerin fuer mutige digitale Produkte.",
        },
    },
    {
        "username": "mira_pm",
        "password": "demo12345",
        "email": "mira@example.com",
        "first_name": "Mira",
        "last_name": "Scholz",
        "profile": {
            "type": "customer",
            "description": "Ich buche Leistungen fuer kleine Produktteams und MVPs.",
        },
    },
    {
        "username": "noah_backend",
        "password": "demo12345",
        "email": "noah@example.com",
        "first_name": "Noah",
        "last_name": "Fischer",
        "profile": {
            "type": "business",
            "location": "Koeln",
            "tel": "+49 221 555 0111",
            "working_hours": "Mo-Fr 08:30-16:30",
            "description": "Backend und Automations-Fokus fuer interne Tools, APIs und Datenfluesse.",
        },
    },
    {
        "username": "sophie_seo",
        "password": "demo12345",
        "email": "sophie@example.com",
        "first_name": "Sophie",
        "last_name": "Wagner",
        "profile": {
            "type": "business",
            "location": "Muenchen",
            "tel": "+49 89 555 0164",
            "working_hours": "Di-Sa 09:00-17:00",
            "description": "SEO, Content-Struktur und Conversion-orientierte Website-Optimierung.",
        },
    },
]


class Command(BaseCommand):
    help = "Seed idempotent demo users, offers, orders, and reviews."

    def handle(self, *args, **options):
        users = {user["username"]: self.ensure_user(user) for user in DEMO_USERS}

        kevin_offer = self.ensure_offer(
            user=users["kevin"],
            title="Business Website Sprint",
            description="Moderne Firmenwebsite mit Kontaktbereich, responsivem Layout und sauberem Setup.",
            details=[
                self.detail_payload("basic", "Starter Onepager", 2, 5, "699.00", [
                    "Onepager mit Kontaktbereich",
                    "Responsive Umsetzung",
                    "Basis-SEO",
                ]),
                self.detail_payload("standard", "Growth Website", 4, 7, "1299.00", [
                    "Bis zu 5 Unterseiten",
                    "CMS-Anbindung",
                    "Onpage-SEO",
                ]),
                self.detail_payload("premium", "Full Funnel Site", 6, 10, "2199.00", [
                    "Landingpage-Funnel",
                    "Terminbuchung",
                    "Analytics-Setup",
                ]),
            ],
        )

        lara_offer = self.ensure_offer(
            user=users["lara_design"],
            title="Branding and UI Kit",
            description="Visuelle Identitaet mit Komponentenbibliothek fuer Produktseiten und Dashboards.",
            details=[
                self.detail_payload("basic", "Mini Brand Kit", 2, 4, "499.00", [
                    "Farbsystem",
                    "Typografie",
                    "Logo-Anpassung",
                ]),
                self.detail_payload("standard", "UI Starter Kit", 3, 6, "999.00", [
                    "Designsystem-Basis",
                    "8 Kernscreens",
                    "Komponenten",
                ]),
                self.detail_payload("premium", "Product UI System", 5, 9, "1699.00", [
                    "Erweitertes UI-Kit",
                    "Design Tokens",
                    "Prototyping",
                ]),
            ],
        )

        noah_offer = self.ensure_offer(
            user=users["noah_backend"],
            title="Custom API Integration",
            description="Planung und Umsetzung belastbarer Schnittstellen fuer Webapps und interne Systeme.",
            details=[
                self.detail_payload("basic", "Webhook Setup", 2, 4, "549.00", [
                    "Ein externer Dienst",
                    "Webhook-Verarbeitung",
                    "Basis-Logging",
                ]),
                self.detail_payload("standard", "API Workflow", 3, 7, "1199.00", [
                    "Mehrere Endpunkte",
                    "Validierung",
                    "Fehlerhandling",
                ]),
                self.detail_payload("premium", "System Integration", 5, 12, "2290.00", [
                    "Mehrsystem-Anbindung",
                    "Retry-Logik",
                    "Monitoring",
                ]),
            ],
        )

        sophie_offer = self.ensure_offer(
            user=users["sophie_seo"],
            title="SEO Landing Page Upgrade",
            description="Struktur, Texte und Onpage-Optimierung fuer mehr Sichtbarkeit und bessere Conversion.",
            details=[
                self.detail_payload("basic", "SEO Audit Light", 2, 3, "349.00", [
                    "Keyword-Check",
                    "Meta-Optimierung",
                    "Kurzbericht",
                ]),
                self.detail_payload("standard", "Landing Page Refresh", 3, 5, "790.00", [
                    "Headline-Optimierung",
                    "Informationsarchitektur",
                    "CTA-Verbesserung",
                ]),
                self.detail_payload("premium", "Conversion SEO Package", 4, 8, "1390.00", [
                    "Komplette Seitenueberarbeitung",
                    "Keyword-Mapping",
                    "Content-Briefing",
                ]),
            ],
        )

        self.ensure_order(
            customer_user=users["andrey"],
            business_user=users["kevin"],
            title="Business Website Sprint",
            revisions=4,
            delivery_time_in_days=7,
            price="1299.00",
            features=[
                "Bis zu 5 Unterseiten",
                "CMS-Anbindung",
                "Onpage-SEO",
            ],
            offer_type="standard",
            status="in_progress",
        )

        self.ensure_order(
            customer_user=users["mira_pm"],
            business_user=users["lara_design"],
            title="Branding and UI Kit",
            revisions=5,
            delivery_time_in_days=9,
            price="1699.00",
            features=[
                "Erweitertes UI-Kit",
                "Design Tokens",
                "Prototyping",
            ],
            offer_type="premium",
            status="completed",
        )

        self.ensure_review(
            business_user=users["kevin"],
            reviewer=users["andrey"],
            rating=5,
            description="Schnelle Kommunikation, saubere Umsetzung und puenktliche Lieferung.",
        )
        self.ensure_review(
            business_user=users["lara_design"],
            reviewer=users["mira_pm"],
            rating=4,
            description="Starkes Gespuer fuer Stil und ein sehr strukturiertes Design-Hand-off.",
        )
        self.ensure_review(
            business_user=users["noah_backend"],
            reviewer=users["andrey"],
            rating=5,
            description="Technisch sehr sauber, gutes API-Design und klare Kommunikation im Projekt.",
        )
        self.ensure_review(
            business_user=users["sophie_seo"],
            reviewer=users["mira_pm"],
            rating=4,
            description="Schnelle SEO-Verbesserungen mit sofort verstaendlichen Empfehlungen.",
        )

        self.stdout.write(self.style.SUCCESS("Demo content seeded successfully."))

    def ensure_user(self, payload):
        user, created = User.objects.get_or_create(
            username=payload["username"],
            defaults={
                "email": payload["email"],
                "first_name": payload["first_name"],
                "last_name": payload["last_name"],
            },
        )
        if created or not user.password:
            user.set_password(payload["password"])
            user.email = payload["email"]
            user.first_name = payload["first_name"]
            user.last_name = payload["last_name"]
            user.save()

        profile, _ = UserProfile.objects.get_or_create(
            username=user,
            defaults=payload["profile"],
        )
        for key, value in payload["profile"].items():
            setattr(profile, key, value)
        profile.save()
        return user

    def ensure_offer(self, user, title, description, details):
        offer, _ = Offer.objects.get_or_create(
            user=user,
            title=title,
            defaults={"description": description},
        )
        offer.description = description
        offer.save(update_fields=["description"])

        for detail in details:
            detail_obj, _ = OfferDetail.objects.get_or_create(
                offer=offer,
                offer_type=detail["offer_type"],
                defaults=detail,
            )
            for key, value in detail.items():
                setattr(detail_obj, key, value)
            detail_obj.save()

        return offer

    def ensure_order(
        self,
        customer_user,
        business_user,
        title,
        revisions,
        delivery_time_in_days,
        price,
        features,
        offer_type,
        status,
    ):
        Order.objects.update_or_create(
            customer_user=customer_user,
            business_user=business_user,
            title=title,
            offer_type=offer_type,
            defaults={
                "revisions": revisions,
                "delivery_time_in_days": delivery_time_in_days,
                "price": price,
                "features": features,
                "status": status,
            },
        )

    def ensure_review(self, business_user, reviewer, rating, description):
        Review.objects.update_or_create(
            business_user=business_user,
            reviewer=reviewer,
            defaults={
                "rating": rating,
                "description": description,
            },
        )

    def detail_payload(self, offer_type, title, revisions, delivery_time, price, features):
        return {
            "offer_type": offer_type,
            "title": title,
            "revisions": revisions,
            "delivery_time_in_days": delivery_time,
            "price": price,
            "features": features,
        }
