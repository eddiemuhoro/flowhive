"""
Generate VAPID keys for push notifications
Run this once and add the keys to your .env file
"""

try:
    from py_vapid import Vapid
    from cryptography.hazmat.primitives import serialization
    import base64

    # Generate new VAPID keys
    vapid = Vapid()
    vapid.generate_keys()

    # Export private key as PEM format
    private_key_pem = vapid.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # Export public key as base64url (URL-safe base64 without padding)
    public_key_bytes = vapid.public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')

    print("\n" + "="*60)
    print("VAPID Keys Generated Successfully!")
    print("="*60)
    print("\nAdd these to your backend/.env file:\n")
    print(f"VAPID_PRIVATE_KEY={private_key_pem}")
    print(f"VAPID_PUBLIC_KEY={public_key_b64}")
    print(f"VAPID_CLAIM_EMAIL=admin@flowhive.app")
    print("\n⚠️  IMPORTANT: Keep the private key secret!")
    print("="*60 + "\n")

except ImportError as e:
    print("\n❌ Required package not installed!")
    print(f"\nError: {e}")
    print("\nInstall it first:")
    print("  pip install pywebpush==1.14.1")
    print("\nThen run this script again.")
except Exception as e:
    print(f"\n❌ Error generating keys: {e}")
    print("\nTry using the online generator instead:")
    print("  https://vapidkeys.com/")
