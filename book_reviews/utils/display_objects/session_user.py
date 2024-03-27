class SessionUser:

    def __init__(self, uid, created_at, username, email, picture):
        self.uid = uid
        self.created_at = created_at
        self.username = username
        self.email = email
        self.picture = picture
    
    @staticmethod
    def from_auth0(uid, created_at, auth0_response):
        userinfo = auth0_response.get("userinfo", {})
        return SessionUser(
            uid=uid,
            created_at=created_at,
            username=userinfo.get("username"),
            email=userinfo.get("email"),
            picture=userinfo.get("picture")
        )
    
    def to_dict(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "email": self.email,
            "picture": self.picture,
            "created_at": self.created_at.isoformat()
        }
