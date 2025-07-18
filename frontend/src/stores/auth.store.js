import { defineStore } from "pinia";

import jwt_decode from "jwt-decode";

import { fetchWrapper } from "@/helpers";
import { router } from "@/router";

export const useAuthStore = defineStore({
  id: "auth",
  state: () => {
    const decodedStr = localStorage.getItem("decoded_access_token");
    const decoded = decodedStr ? JSON.parse(decodedStr) : {};

    return {
      access_token: localStorage.getItem("access_token"),
      decoded_access_token: decoded,
      scopes: decoded.scopes || [],
      returnUrl: null,
    };
  },
  actions: {
    async authenticate(username, password) {
      const response = await fetchWrapper.authenticate(username, password);

      this.access_token = response.access_token;
      this.decoded_access_token = jwt_decode(this.access_token);
      this.scopes = this.decoded_access_token.scopes;

      localStorage.setItem("access_token", this.access_token);

      localStorage.setItem(
        "decoded_access_token",
        JSON.stringify(this.decoded_access_token),
      );

      router.push("/");
    },
    isAuthenticated() {
      return (
        !!this.access_token &&
        !!this.decoded_access_token &&
        this.decoded_access_token.exp > Date.now() / 1000
      );
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$reset();
      router.push("/login");
    },
  },
});
