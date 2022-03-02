
const admin = require('firebase-admin')
const serviceAccount = require('../serviceAccountKey.json')
const functions = require("firebase-functions")

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://project-friendship-lamp-default-rtdb.firebaseio.com',
})

const db = admin.database()

// Helper to get the authed user id from a request
const getUid = async (req, res) => {
  const authToken = req.get('Authorization')?.split('Bearer ')[1]

  if (!authToken) {
    res.status(401).send('Unauthorized')
    return
  }

  const decodedToken = await admin.auth().verifyIdToken(authToken)
  return decodedToken.uid
}

const toKebab = (str) => {
  return str
    .replaceAll(' ', '-')
    .replace(/[^a-zA-Z,-]/g, '')
    .toLowerCase()
}

exports.createLamp = functions.https.onCall(async (data, context) => {
  
    try {
      const uid = context.auth.uid

      if (!uid) {
        throw new functions.https.HttpsError(
          'unauthenticated',
          'You must be signed in.',
        )
      }

      let { groupId } = data
      const { accessCode, deviceData } = data

      if (!groupId || !deviceData || !deviceData.deviceId) {
        throw new functions.https.HttpsError(
          'invalid-argument',
          'Missing required fields.',
        )
      }

      let creatingGroup = false
      if (!accessCode) {
        creatingGroup = true
      }
    
      // Convert group ID to kebab case
      groupId = toKebab(groupId)
    
      // Check if the group exists
      const groupRef = db.ref(`/groups/${groupId}`)
      const groupSnapshot = await groupRef.once('value')
    
      const groupExists = groupSnapshot.exists()
    
      // Creating a group that already exists
      if (creatingGroup && groupExists) {
        throw new functions.https.HttpsError(
          'already-exists',
          'Group already exists.',
        )
      }
    
      // Joining a group that doesn't exist
      if (!creatingGroup && !groupExists) {
        throw new functions.https.HttpsError(
          'not-found',
          'Group does not exist.',
        )
      }
    
      let group
    
      if (groupExists) {
        group = groupSnapshot.val()
        
        // Check access code is correct
        if (group.accessCode !== accessCode) {
          throw new functions.https.HttpsError(
            'permission-denied',
            'Invalid access code.',
          )

        }
      }
      else {
        // Generate a random access code
        const newAccessCode = Math.floor(Math.random() * 1000000).toString()
      
        // Create group object
        group = {
          createdAt: Date.now(),
          accessCode: newAccessCode,
        }
        // Create group
        await groupRef.set(group)
      }
    
      // Create lamp object
      const lamp = {
        controls: {
          color: '#ff0000',
          timestamp: Date.now(),
          touching: false,
        },
        userId: uid,
        groupId: groupId,
      }
    
      // Create lamp
      const lampRef = db.ref(`/lamps/${deviceData.deviceId}`)
    
      await lampRef.set(lamp)
    
      return {
        message: 'Lamp created.',
      }
    }
    catch (error) {
      functions.logger.error("Error creating lamp:", error)
      throw new functions.https.HttpsError(
        'internal',
        'Error creating lamp.',
        error
      )
    }  
})


// TODO: Redo this with lamps collection
exports.leaveGroup = functions.https.onCall(async (data, context) => {
  
    const uid = context.auth.uid

    // Get the user's group ID
    const groupIdRef = db.ref(`users/${uid}/groupId`)
    const groupIdSnapshot = await groupIdRef.once('value')

    if (!groupIdSnapshot.exists()) {
      throw new functions.https.HttpsError(
        'not-found',
        'You are not in a group.',
      )
    }
    const groupId = groupIdSnapshot.val()

    // Remove user from group
    await groupIdRef.remove()

    // Remove group if no users are left in it
    const snapshot = await db
      .ref('users')
      .orderByChild('groupId')
      .equalTo(groupId)
      .once('value')

    if (!snapshot.exists()) {
      db.ref(`groups/${groupId}`).remove()
    }

    return {
      'success': true,
    }
})
