"""
Case 1 — Envio do e-mail semanal pelo Gmail.

Lê as credenciais de avancado/case1_focus/.env (copie .env.exemplo para .env e preencha).
O .env NUNCA vai para o GitHub: o .gitignore já o ignora.

Teste sozinho:
    python avancado/case1_focus/enviar_email.py
"""
import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ENV = Path(__file__).resolve().parent / ".env"


def ler_env(caminho: Path = ENV) -> dict:
    if not caminho.exists():
        raise SystemExit(f"Arquivo {caminho} não encontrado. Copie .env.exemplo para .env e preencha.")
    cfg = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            chave, valor = linha.split("=", 1)
            cfg[chave.strip()] = valor.strip().strip('"').strip("'")
    for chave in ("GMAIL_USUARIO", "GMAIL_SENHA_DE_APP", "DESTINATARIOS"):
        if not cfg.get(chave):
            raise SystemExit(f"Falta {chave} no .env")
    return cfg


def enviar(assunto: str, html: str, imagens: dict[str, Path] | None = None) -> list[str]:
    """Envia o e-mail. `imagens` mapeia um identificador para o arquivo da imagem;
    no HTML, referencie cada uma como <img src="cid:identificador">.

    Imagens vão anexadas em vez de embutidas em base64 porque o Gmail não exibe
    data URI dentro de e-mail.
    """
    cfg = ler_env()
    destinatarios = [d.strip() for d in cfg["DESTINATARIOS"].split(",") if d.strip()]

    msg = MIMEMultipart("related")
    msg["Subject"], msg["From"], msg["To"] = assunto, cfg["GMAIL_USUARIO"], ", ".join(destinatarios)
    corpo = MIMEMultipart("alternative")
    corpo.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(corpo)

    for cid, caminho in (imagens or {}).items():
        caminho = Path(caminho)
        if not caminho.exists():
            raise SystemExit(f"Imagem {caminho} não encontrada.")
        img = MIMEImage(caminho.read_bytes())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=caminho.name)
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(cfg["GMAIL_USUARIO"], cfg["GMAIL_SENHA_DE_APP"].replace(" ", ""))
        s.sendmail(cfg["GMAIL_USUARIO"], destinatarios, msg.as_string())
    return destinatarios


if __name__ == "__main__":
    para = enviar("Teste do agente do Focus", "<p>Se você recebeu isto, o envio está funcionando.</p>")
    print("E-mail de teste enviado para", ", ".join(para))
