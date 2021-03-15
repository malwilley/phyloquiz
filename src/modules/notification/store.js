import { writable } from 'svelte/store'
import { filter } from 'ramda'
import delay from '../../utils/delay'
import { nanoid } from 'nanoid'

export const notifications = writable([])

export const actions = {
  pushNotification: async ({ message, type = 'error', duration = 5000 }) => {
    const notification = { id: nanoid(), message, type }

    notifications.update(($notifications) => [...$notifications, notification])

    await delay(duration)

    actions.popNotification(notification.id)
  },
  popNotification: (id) => {
    notifications.update(($notifications) =>
      filter((n) => n.id !== id, $notifications),
    )
  },
}
