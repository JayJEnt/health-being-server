VERIFICATION_TEMPLATE = {
    "subject": "Verify your email address",
    "body": """
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
            <div style="max-width: 400px; margin: auto; background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">Email verification</h2>
                <p style="font-size: 16px;">Use the link below to verify your email:</p>
                <div style="font-size: 24px; font-weight: bold; color: #007bff; text-align: center; margin: 20px 0;">
                    <a href="{verification_link}">Verify Email</a>
                </div>
                <p style="font-size: 14px; color: #666;">This link expires in {expire_time} minutes.</p>
            </div>
        </body>
    </html>
    """,
}
