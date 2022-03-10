export interface User {
  _id: string,
  googleId: string;
  name: string;
  familyName: string;
  givenName: string;
  email?: string;
  picture?: string;
}