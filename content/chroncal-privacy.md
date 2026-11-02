+++
title = 'Chroncal Personal privacy policy'
description = 'How Christopher Lamm’s private Chroncal Google Calendar integration handles Google user data.'
url = '/chroncal/privacy/'
draft = false
+++

Effective November 2, 2026.

This policy covers [Chroncal Personal](/chroncal/), the Google Calendar OAuth
integration operated by Christopher Lamm for my own personal and work calendars.
It describes my use of the upstream
[Chroncal application](https://github.com/DouglasdeMoura/chroncal), not every
deployment of that project or Google’s own services.

## Data access and use

After I authorize access through Google, Chroncal can discover calendars available
to my account and download calendar metadata and event data. This can include
calendar names and identifiers, account email addresses, event titles,
descriptions, dates, times, locations, organizers, attendees, recurrence rules,
reminders, and other fields included in calendar records. OAuth access and refresh
tokens allow it to connect and continue syncing without repeated sign-in.

The requested scope is `https://www.googleapis.com/auth/calendar`. It permits
viewing, editing, sharing, and permanently deleting calendars accessible to the
authorized account. I use it to display calendars locally and synchronize event
creations, edits, and deletions with Google, subject to the account’s permissions.
Calendar selection in Chroncal controls sync, not the breadth of Google’s grant.
This integration does not request access to Gmail messages or Google Drive files.

## Storage and protection

Calendar records and synchronization metadata are stored in Chroncal’s local
SQLite database on my computer. Credentials, including OAuth tokens and the
client secret, use the operating system keyring by default, according to
Chroncal’s documentation. Chroncal also supports plaintext credential files when
enabled or retained from an earlier configuration. Local storage should not be
assumed to be encrypted by Chroncal; protection also depends on the computer,
keyring, and any disk encryption or backups I configure.

Authorization and calendar synchronization communicate with Google over HTTPS.
There is no integration server operated by me. This informational website does
not receive or store OAuth tokens or calendar records.

## Sharing and other uses

Data moves between my local Chroncal installation and Google to provide calendar
sync. Changes sent to Google remain subject to the calendar’s existing sharing
settings and may be visible to attendees or people with access to that calendar.

I do not sell Google user data, use it for advertising, send it to AI services, or
use it to train AI models. I do not provide it to the upstream Chroncal maintainers
or other third parties through this integration. Copies I make through local
exports or computer backups remain under my control and must be managed separately.

My use of information received from Google APIs follows the
[Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy),
including its Limited Use requirements.

## Retention, deletion, and revocation

Local calendar data is kept while I use the integration, until I remove it. There
is no automatic deletion schedule. Tokens are retained for ongoing sync until
removed or invalidated; Google may expire or revoke them.

To stop access, open [Google Account connections](https://myaccount.google.com/connections),
select this integration, and remove its access. Stop any Chroncal background sync
and remove the account in Chroncal as well. Revocation prevents future authorized
access but does not erase previously downloaded records. Chroncal’s documented
account-removal behavior retains downloaded calendars as local copies.

To remove those copies, disconnect the account first, then remove the retained
local calendars and any related database copies, exports, backups, or remaining
credentials. Deleting an event while it is still connected can synchronize that
deletion to Google. Revoking access or removing local copies does not itself
delete the calendars or events held by Google.

## Contact and changes

For privacy questions or deletion assistance, contact Christopher Lamm at
[christopherlamm81@gmail.com](mailto:christopherlamm81@gmail.com).
I will update this page and its effective date if this integration’s data handling
changes, and obtain renewed consent before using Google data for a new purpose.
