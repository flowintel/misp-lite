<script setup>
import { Form, Field } from "vee-validate";
import { storeToRefs } from "pinia";
import { useUsersStore } from "@/stores";
import { router } from "@/router";
import { UserSchema } from "@/schemas/user";
import RolesSelect from "@/components/roles/RolesSelect.vue";
import OrganisationsSelect from "@/components/organisations/OrganisationsSelect.vue";

const usersStore = useUsersStore();
const { user, status } = storeToRefs(usersStore);

function onSubmit(values, { setErrors }) {
  return usersStore
    .update(values.user)
    .then(() => {
      router.push(`/users/${values.user.id}`);
    })
    .catch((error) => setErrors({ apiError: error }));
}

function handleRoleUpdated(roleId) {
  user.role_id = roleId;
}
function handleOrganisationUpdated(orgId) {
  user.org_id = orgId;
}
</script>

<template>
  <div class="card">
    <div class="card-header border-bottom">
      <div class="row">
        <div class="col-10">
          <h3>Update User</h3>
        </div>
      </div>
    </div>
    <div class="card-body d-flex flex-column">
      <Form
        @submit="onSubmit"
        :validation-schema="UserSchema"
        v-slot="{ errors }"
      >
        <div class="mb-3">
          <label for="user.id">id</label>
          <Field
            class="form-control"
            id="user.id"
            name="user.id"
            v-model="user.id"
            :class="{ 'is-invalid': errors['user.id'] }"
            disabled
          >
          </Field>
          <div class="invalid-feedback">{{ errors["organisation.id"] }}</div>
        </div>
        <div class="mb-3">
          <label for="user.email">email</label>
          <Field
            class="form-control"
            id="user.email"
            name="user.email"
            v-model="user.email"
            :class="{ 'is-invalid': errors['user.email'] }"
          >
          </Field>
          <div class="invalid-feedback">{{ errors["user.email"] }}</div>
        </div>
        <div class="mb-3">
          <label for="user.org_id">organisation</label>
          <OrganisationsSelect
            name="user.org_id"
            :selected="user.org_id"
            @organisation-updated="handleOrganisationUpdated"
            :errors="errors['user.org_id']"
          />
          <div class="invalid-feedback">{{ errors["user.org_id"] }}</div>
        </div>
        <div class="mb-3">
          <label for="user.role_id">role</label>
          <RolesSelect
            name="user.role_id"
            :selected="user.role_id"
            @role-updated="handleRoleUpdated"
            :errors="errors['user.role_id']"
          />
          <div class="invalid-feedback">{{ errors["user.role_id"] }}</div>
        </div>
        <div v-if="errors.apiError" class="w-100 alert alert-danger mt-3 mb-3">
          {{ errors.apiError }}
        </div>
        <button
          type="submit"
          class="btn btn-outline-primary"
          :class="{ disabled: status.updating }"
        >
          <span v-if="status.updating">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            ></span>
          </span>
          <span v-if="!status.updating">Save</span>
        </button>
      </Form>
    </div>
  </div>
</template>
