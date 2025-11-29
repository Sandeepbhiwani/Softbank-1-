from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from accounts.models import CustomUser
from stockmanagement.models import Stock
from assets.models import Position
from assets.models import order  # adjust this import if your order model is elsewhere

class Command(BaseCommand):
    help = "Generate dummy stock data, orders, and portfolio for existing users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Generating 100 dummy stocks..."))

        # Create 100 dummy stocks
        stock_symbols = [f"STOCK{i}" for i in range(1, 101)]
        stock_objs = []

        for symbol in stock_symbols:
            stock = Stock(
                symbol=symbol,
                name=f"Company {symbol}",
                current_price=Decimal(round(random.uniform(100, 2000), 2))
            )
            stock_objs.append(stock)

        Stock.objects.bulk_create(stock_objs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("✅ 100 dummy stocks created."))

        # Get all stocks and users
        all_stocks = list(Stock.objects.all())
        users = list(CustomUser.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Please create users first."))
            return

        self.stdout.write(self.style.WARNING("Generating dummy positions and orders..."))

        for user in users:
            # Each user gets 5–10 random positions
            for _ in range(random.randint(5, 10)):
                stock = random.choice(all_stocks)
                quantity = random.randint(1, 100)
                buy_price = round(random.uniform(100, 1500), 2)
                sell_price = round(buy_price + random.uniform(-50, 150), 2)

                pos = Position.objects.create(
                    user=user,
                    stock=stock,
                    quantity=quantity,
                    last_traded_quantity=quantity,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    realised_pnl=(sell_price - buy_price) * quantity,
                    last_traded_datetime=timezone.now(),
                    is_closed=random.choice([True, False])
                )

                # Create related dummy order
                order_type = random.choice(["BUY", "SELL"])
                status = random.choice(["initiated", "pending", "completed", "cancelled", "failed"])
                price = sell_price if order_type == "SELL" else buy_price
                amount = price * quantity
                charges = round(amount * 0.001, 2)  # 0.1% brokerage

                order.objects.create(
                    user=user,
                    stock=stock,
                    price=price,
                    quantity=quantity,
                    amount=amount,
                    order_type=order_type,
                    charges=charges,
                    status=status,
                    position=pos
                )

        self.stdout.write(self.style.SUCCESS("🎉 Dummy positions and orders generated successfully!"))
