+++
title = 'Chroncal Personal'
description = 'Christopher Lamm’s private Google Calendar integration using Chroncal.'
url = '/chroncal/'
draft = false
+++

Chroncal Personal is my privately operated Google Calendar OAuth integration. I’m
Christopher Lamm, and I use it to view and manage my own personal and work calendars
from [Chroncal](https://github.com/DouglasdeMoura/chroncal), a terminal calendar
application maintained by Douglas de Moura and its contributors. I operate this
OAuth configuration; I do not own or maintain the upstream Chroncal project.

## What it does

Chroncal runs on my computer, stores calendar data locally, and synchronizes events
with Google Calendar through CalDAV. I use it to read events and to create, edit,
and delete events on calendars where my Google account has permission. This
integration is for my own use and is not a public sign-up service.

Google handles sign-in and consent in the browser. The integration requests
`https://www.googleapis.com/auth/calendar`, the scope documented by Chroncal for
Google Calendar sync. This grants broad permission to view, edit, share, and
permanently delete accessible calendars. My intended use is calendar discovery and
event synchronization; selecting calendars in Chroncal does not narrow the OAuth
permission itself. It does not request Gmail or Google Drive access.

This website provides information about the integration. It does not receive my
Google OAuth tokens or calendar data. The integration is independently operated
and is not endorsed by Google.

## Privacy and contact

Read the [Chroncal Personal privacy policy](/chroncal/privacy/) for details about
data access, storage, sharing, retention, and removing access.

For questions about this integration or its data handling, contact
[Christopher Lamm](mailto:christopherlamm81@gmail.com).
