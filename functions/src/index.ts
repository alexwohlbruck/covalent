const cors = require('cors')({ origin: true })
const admin = require('firebase-admin')
const serviceAccount = require('../serviceAccountKey.json')

import * as functions from 'firebase-functions'

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://friendship-lamp-1ea8a-default-rtdb.firebaseio.com',
})

const db = admin.database()

// Helper to get the authed user id from a request
const getUid = async (req: any, res: any) => {
  const authToken = req.get('Authorization')?.split('Bearer ')[1]

  if (!authToken) {
    res.status(401).send('Unauthorized')
    return
  }

  const decodedToken = await admin.auth().verifyIdToken(authToken)
  return decodedToken.uid
}


export const createGroup = functions.https.onRequest(async (req, res) => {
  cors(req, res, async () => {
    
    const uid = await getUid(req, res)
    if (!uid) return res.status(401).json({
      message: 'You must be signed in.'
    })

    const { groupId } = req.body.data

    const groupRef = db.ref(`/groups/${groupId}`)
    const groupSnapshot = await groupRef.once('value')

    if (groupSnapshot.exists()) {
      return res.status(400).json({
        message: 'Group already exists.'
      })
    }

    const group = {
      createdAt: Date.now(),
      accessCode: Math.floor(Math.random() * 1000000),
      userStates: {
        [uid]: {
          color: '#ff0000',
          timestamp: Date.now(),
          touching: false,
        }
      }
    }

    // Create group
    await groupRef.set(group)

    // Add user to group
    try {
      await db.ref(`users/${uid}`).set({
        groupId,
      })

      return res.status(200).send('OK')
    } catch (e) {
      return res.status(400).json(e)
    }
  })
})

export const joinGroup = functions.https.onRequest(async (req, res) => {
  cors(req, res, async () => {
    const uid = await getUid(req, res)
    let { groupId, accessCode } = req.body.data

    // Convert group ID to kebab case
    groupId = groupId.replaceAll(' ','-').replace(/[^a-zA-Z,-]/g,"").toLowerCase()
    
    // Check if group exists
    const groupRef = db.ref(`groups/${groupId}`)
    const groupSnapshot = await groupRef.once('value')
    if (!groupSnapshot.exists()) {
      res.status(404).send('That group does not exist.')
      return
    }

    // Check that access code is avlid
    const group = groupSnapshot.val()
    if (group.accessCode !== accessCode) {
      res.status(401).json({message: 'Invalid access code.'})
      return
    }

    // Add user to group
    try {
      await db.ref(`users/${uid}`).set({
        groupId,
      })

      return res.status(200).send('OK')
    } catch (e) {
      return res.status(400).json(e)
    }
  })
})

export const leaveGroup = functions.https.onRequest(async (req, res) => {
  cors(req, res, async () => {
    const uid = await getUid(req, res)

    // Get the user's group ID
    const groupIdRef = db.ref(`users/${uid}/groupId`)
    const groupIdSnapshot = await groupIdRef.once('value')
    if (!groupIdSnapshot.exists()) {
      return res.status(404).send('You are not in a group.')
    }
    const groupId = groupIdSnapshot.val()

    // Remove user from group
    await groupIdRef.remove()

    // Remove group if no users are left in it
    const snapshot = await db.ref(`users`).orderByChild('groupId').equalTo(groupId).once('value')
    if (!snapshot.exists()) {
      db.ref(`groups/${groupId}`).remove()
    }
    
    return res.status(200).send('OK')
  })
})
