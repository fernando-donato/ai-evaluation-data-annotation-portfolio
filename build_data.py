"""Regenerate the synthetic bilingual intent-annotation demonstration data."""
from pathlib import Path
import csv
import json

OUT = Path(__file__).parent / "dist" / "data"
OUT.mkdir(parents=True, exist_ok=True)

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

# Fictional customer messages. One primary intent per item. Urgency is a
# demonstrative triage label based solely on language in the message.
examples = [
    ("Meu pedido não chegou e o rastreio parou há uma semana.", "DELIVERY_ISSUE", "Medium"),
    ("Recebi aviso de entrega, mas não há pacote na portaria.", "DELIVERY_ISSUE", "Medium"),
    ("A encomenda veio com dois dias de atraso.", "DELIVERY_ISSUE", "Low"),
    ("Podem confirmar onde está minha entrega?", "DELIVERY_ISSUE", "Low"),
    ("O endereço da entrega está errado e o pacote sai hoje.", "DELIVERY_ISSUE", "High"),
    ("O pacote foi devolvido ao remetente sem tentativa de entrega.", "DELIVERY_ISSUE", "Medium"),
    ("Fui cobrado duas vezes pelo mesmo pedido.", "BILLING_ISSUE", "Medium"),
    ("Meu cartão foi recusado, mas o banco aprovou a compra.", "BILLING_ISSUE", "Medium"),
    ("Quero entender uma taxa extra na fatura.", "BILLING_ISSUE", "Low"),
    ("Minha assinatura cancelada apareceu na fatura deste mês.", "BILLING_ISSUE", "Medium"),
    ("O boleto vence hoje e não consigo gerar a segunda via.", "BILLING_ISSUE", "High"),
    ("A cobrança está em uma moeda diferente da exibida no checkout.", "BILLING_ISSUE", "Medium"),
    ("Quero meu dinheiro de volta pelo produto que devolvi.", "REFUND_REQUEST", "Medium"),
    ("Por favor, estornem a cobrança duplicada no cartão.", "REFUND_REQUEST", "Medium"),
    ("Solicito reembolso da assinatura renovada por engano.", "REFUND_REQUEST", "Medium"),
    ("Paguei por um serviço que não funcionou; podem me devolver o valor?", "REFUND_REQUEST", "Medium"),
    ("Preciso do estorno antes do fechamento da fatura amanhã.", "REFUND_REQUEST", "High"),
    ("Gostaria de saber como pedir reembolso deste pedido.", "REFUND_REQUEST", "Low"),
    ("Esqueci minha senha e não consigo acessar a conta.", "ACCOUNT_ACCESS", "Medium"),
    ("O código de verificação não chega no meu e-mail.", "ACCOUNT_ACCESS", "Medium"),
    ("Minha conta foi bloqueada após várias tentativas.", "ACCOUNT_ACCESS", "Medium"),
    ("Não consigo entrar com meu novo número de telefone.", "ACCOUNT_ACCESS", "Medium"),
    ("Aparece acesso negado quando tento fazer login.", "ACCOUNT_ACCESS", "Medium"),
    ("Como ativo a autenticação de dois fatores?", "ACCOUNT_ACCESS", "Low"),
    ("O aplicativo fecha quando tento abrir meus pedidos.", "TECHNICAL_SUPPORT", "Medium"),
    ("O botão de finalizar compra não responde.", "TECHNICAL_SUPPORT", "Medium"),
    ("A página mostra erro 500 ao enviar o formulário.", "TECHNICAL_SUPPORT", "Medium"),
    ("O site fica em branco no navegador do celular.", "TECHNICAL_SUPPORT", "Medium"),
    ("O arquivo de comprovante não abre depois do download.", "TECHNICAL_SUPPORT", "Low"),
    ("Vocês vendem vale-presente para compras?", "OTHER", "Low"),
    ("Do you ship to rural addresses?", "OTHER", "Low"),
    ("I'd like to suggest a new color option for this product.", "OTHER", "Low"),
    ("My order is stuck in transit and I need it for tomorrow's event.", "DELIVERY_ISSUE", "High"),
    ("Tracking says delivered, but nothing was left at my door.", "DELIVERY_ISSUE", "Medium"),
    ("Can I reroute a package that's already on the way?", "DELIVERY_ISSUE", "Medium"),
    ("The courier went to the wrong apartment.", "DELIVERY_ISSUE", "Medium"),
    ("There's a charge on my statement I don't recognize.", "BILLING_ISSUE", "Medium"),
    ("My promo code wasn't reflected in the final charge.", "BILLING_ISSUE", "Medium"),
    ("The payment failed but my balance was reduced.", "BILLING_ISSUE", "High"),
    ("Please refund the amount charged after I canceled.", "REFUND_REQUEST", "Medium"),
    ("Can you return the shipping fee to my card?", "REFUND_REQUEST", "Medium"),
    ("The item arrived damaged; I'd like my money back.", "REFUND_REQUEST", "Medium"),
    ("I no longer have access to the email tied to my account.", "ACCOUNT_ACCESS", "Medium"),
    ("The reset link keeps saying it has expired.", "ACCOUNT_ACCESS", "Medium"),
    ("Someone else seems to have signed into my account.", "ACCOUNT_ACCESS", "High"),
    ("The app crashes every time I upload a photo.", "TECHNICAL_SUPPORT", "Medium"),
    ("I get an error whenever I try to download my receipt.", "TECHNICAL_SUPPORT", "Low"),
    ("Do you have a student discount?", "OTHER", "Low"),
]

annotation_rows = []
for i, (message, label, urgency) in enumerate(examples, 1):
    lang = "pt-BR" if i <= 30 else "en"
    annotation_rows.append(dict(item_id=f"AN-{i:03d}", language=lang, text=message,
                                primary_intent=label, urgency=urgency, provenance="synthetic"))
write_csv(OUT / "intent_annotations.csv", annotation_rows)
(OUT / "intent_annotations.json").write_text(
    json.dumps(annotation_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"Exported {len(annotation_rows)} synthetic annotation records")
