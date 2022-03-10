
export createLamp = async   ({ dispatch }, {
  groupId, accessCode, deviceData
}: {
  groupId: string,
  accessCode: string,
  deviceData: any
}) {
  try {
    // TODO
    // const result = await createLamp({
    //   groupId,
    //   accessCode,
    //   deviceData,
    // })
    // router.push({name: 'lamps'})
    // return result
  }
  catch (error: any) {
    dispatch('error', error?.details?.message)
  }
}