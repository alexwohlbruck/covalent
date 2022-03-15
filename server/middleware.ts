export const isAuthenticated = (req: any, res: any, next: any) => {
  if (req.isAuthenticated()) {
    return next()
  }
  return res.status(401).json({
    message: `You aren't signed in!`,
  })
}