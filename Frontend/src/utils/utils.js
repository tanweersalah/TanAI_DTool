// utils.js

import { format, parseISO } from "date-fns";

export function formatTimestamp(timestamp) {
  try {
    const date = parseISO(timestamp);
    return format(date, "MMMM d, yyyy HH:mm:ss");
  } catch (error) {
    console.error("Error formatting timestamp:", error);
    return "Invalid Date";
  }
}

export function formatRelativeTime(timestamp) {
  try {
    const date = parseISO(timestamp);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return `${diffInSeconds} seconds ago`;
    if (diffInSeconds < 3600)
      return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400)
      return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 2592000)
      return `${Math.floor(diffInSeconds / 86400)} days ago`;

    return format(date, "MMMM d, yyyy");
  } catch (error) {
    console.error("Error formatting relative time:", error);
    return "Invalid Date";
  }
}

export function isValidTimestamp(timestamp) {
  try {
    parseISO(timestamp);
    return true;
  } catch {
    return false;
  }
}
