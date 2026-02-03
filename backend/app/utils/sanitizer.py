"""
HTML Sanitization Utilities
Sanitize user-provided HTML content to prevent XSS attacks
"""
import bleach
from typing import Optional


# Allowed HTML tags for rich text content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'hr', 'a', 'span', 'div'
]

# Allowed HTML attributes
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'span': ['class'],
    'div': ['class'],
}

# Allowed CSS styles (if needed in the future)
ALLOWED_STYLES = []


def sanitize_html(html_content: Optional[str]) -> Optional[str]:
    """
    Sanitize HTML content to prevent XSS attacks.

    Args:
        html_content: Raw HTML string from user input

    Returns:
        Sanitized HTML string safe for storage and display
    """
    if not html_content:
        return html_content

    # Use bleach to sanitize the HTML
    cleaned_html = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,  # Strip disallowed tags instead of escaping
    )

    return cleaned_html


def strip_html_tags(html_content: Optional[str]) -> str:
    """
    Strip all HTML tags and return plain text.
    Useful for previews or search indexing.

    Args:
        html_content: HTML string

    Returns:
        Plain text without any HTML tags
    """
    if not html_content:
        return ""

    # Remove all HTML tags
    return bleach.clean(html_content, tags=[], strip=True)
