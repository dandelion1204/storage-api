// static/js/auth.js
class AuthService {
    static TOKEN_KEY = 'token';
    static USER_KEY = 'user';

    static getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    static getUser() {
        const userStr = localStorage.getItem(this.USER_KEY);
        return userStr ? JSON.parse(userStr) : null;
    }

    static setAuth(token, user) {
        localStorage.setItem(this.TOKEN_KEY, token);
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    }

    static clearAuth() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    }

    static async checkAuth() {
        const token = this.getToken();
        if (!token) return false;

        try {
            const response = await fetch('/api/user/me/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            if (!response.ok) {
                this.clearAuth();
                return false;
            }

            const userData = await response.json();
            this.setAuth(token, userData);
            return true;
        } catch (error) {
            this.clearAuth();
            return false;
        }
    }

    static async login(email, password) {
        const tokenResponse = await fetch('/api/user/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        if (!tokenResponse.ok) {
            throw new Error('登入失敗');
        }

        const { token } = await tokenResponse.json();

        const userResponse = await fetch('/api/user/me/', {
            headers: {
                'Authorization': `Token ${token}`
            }
        });

        if (!userResponse.ok) {
            throw new Error('取得用戶資料失敗');
        }

        const userData = await userResponse.json();
        this.setAuth(token, userData);
        return userData;
    }

    static logout() {
        this.clearAuth();
        window.location.href = '/login';
    }
}

// 確保 AuthService 是全局可用的
window.AuthService = AuthService;