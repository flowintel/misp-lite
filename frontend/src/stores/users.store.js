import { defineStore } from "pinia";

import { fetchWrapper } from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    users: {},
    user: {},
    status: {
      loading: false,
      creating: false,
      error: false,
    },
  }),
  actions: {
    async getAll() {
      this.status = { loading: true };
      fetchWrapper
        .get(baseUrl)
        .then((users) => (this.users = users))
        .catch((error) => (this.status = { error }))
        .finally(() => (this.status = { loading: false }));
    },
    async getById(id) {
      this.status = { loading: true };
      fetchWrapper
        .get(`${baseUrl}/${id}`)
        .then((user) => (this.user = user))
        .catch((error) => (this.status = { error }))
        .finally(() => (this.status = { loading: false }));
    },
    async create(user) {
      this.status = { creating: true };
      return await fetchWrapper
        .post(baseUrl, user)
        .then((response) => (this.user = response))
        .finally(() => (this.status = { creating: false }));
    },
    async update(organisation) {
      this.status = { updating: true };
      fetchWrapper
        .patch(`${baseUrl}/${organisation.id}`, organisation)
        .then((response) => (this.organisation = response))
        .catch((error) => (this.error = error))
        .finally(() => (this.status = { updating: false }));
    },
    async delete(id) {
      this.status = { loading: true };
      return await fetchWrapper
        .delete(`${baseUrl}/${id}`)
        .catch((error) => (this.status = { error }))
        .finally(() => (this.status = { loading: false }));
    },
  },
});
