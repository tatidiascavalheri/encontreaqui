class PaymentProvider:
    def create_intent(self, amount_cents: int, currency: str = "brl") -> dict:
        return {
            "provider": "stripe",
            "payment_intent_id": f"pi_mock_{amount_cents}",
            "status": "requires_capture",
            "currency": currency,
            "amount_cents": amount_cents,
        }
