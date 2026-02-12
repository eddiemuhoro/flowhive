// Date and time utility functions
// All dates from backend are in UTC and need to be converted to local time for display

/**
 * Formats a UTC datetime string to local date and time
 * @param utcDateString - ISO datetime string from backend (UTC)
 * @returns Formatted local date and time string
 */
export function formatDateTime(utcDateString: string | null | undefined): string {
  if (!utcDateString) return 'N/A';

  const date = new Date(utcDateString + 'Z'); // Append 'Z' to indicate UTC
  return date.toLocaleString('en-KE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Africa/Nairobi'
  });
}

/**
 * Formats a UTC datetime string to local date only
 * @param utcDateString - ISO datetime string from backend (UTC)
 * @returns Formatted local date string
 */
export function formatDate(utcDateString: string | null | undefined): string {
  if (!utcDateString) return 'N/A';

  const date = new Date(utcDateString + 'Z'); // Append 'Z' to indicate UTC
  return date.toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'Africa/Nairobi'
  });
}

/**
 * Formats a UTC datetime string to local time only
 * @param utcDateString - ISO datetime string from backend (UTC)
 * @returns Formatted local time string
 */
export function formatTime(utcDateString: string | null | undefined): string {
  if (!utcDateString) return 'N/A';

  const date = new Date(utcDateString + 'Z'); // Append 'Z' to indicate UTC
  return date.toLocaleTimeString('en-KE', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Africa/Nairobi'
  });
}

/**
 * Formats a UTC datetime string to relative time (e.g., "2 hours ago")
 * @param utcDateString - ISO datetime string from backend (UTC)
 * @returns Relative time string
 */
export function formatRelativeTime(utcDateString: string | null | undefined): string {
  if (!utcDateString) return 'N/A';

  const date = new Date(utcDateString + 'Z'); // Append 'Z' to indicate UTC
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

  return formatDate(utcDateString);
}

/**
 * Formats activity time (HH:MM:SS) to 12-hour format
 * Note: Activity times are already in local timezone
 * @param timeString - Time string in HH:MM:SS format
 * @returns Formatted time in 12-hour format
 */
export function formatActivityTime(timeString: string | null | undefined): string {
  if (!timeString) return 'N/A';

  const [hours, minutes] = timeString.split(':');
  const hour = parseInt(hours, 10);
  const period = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;

  return `${displayHour}:${minutes} ${period}`;
}
