export const db = {
  username: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  cluster: process.env.DB_CLUSTER,
  dbName: process.env.DB_NAME,
  connectionString() {
    return `mongodb+srv://${this.username}:${this.password}@${this.cluster}.mongodb.net/${this.dbName}?retryWrites=true&w=majority`
  },
}
