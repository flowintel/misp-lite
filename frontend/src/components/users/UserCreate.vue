<script setup>
import { Form, Field } from "vee-validate";
import { storeToRefs } from 'pinia'
import { useUsersStore } from "@/stores";
import { router } from "@/router";
import { UserSchema } from "@/schemas/user";

const usersStore = useUsersStore();
const { status, error } = storeToRefs(usersStore);

let user = {};

function onSubmit(values, { setErrors }) {
    return usersStore
        .create(user)
        .then((response) => {
            router.push(`/users/${response.id}`);
        })
        .catch((error) => setErrors({ apiError: error }));
}
</script>

<template>
    <div class="card">
        <div class="card-header border-bottom">
            <div class="row">
                <div class="col-10">
                    <h3>Create User</h3>
                </div>
            </div>
        </div>
        <div class="card-body d-flex flex-column">
            <Form @submit="onSubmit" :validation-schema="UserSchema" v-slot="{ errors, isSubmitting }">
                <div class="mb-3">
                    <label for="user.email">email</label>
                    <Field class="form-control" id="user.email" name="user.email" v-model="user.email"
                        :class="{ 'is-invalid': errors['user.email'] }">
                    </Field>
                    <div class=" invalid-feedback">{{ errors['user.email'] }}</div>
                </div>
                <div class="mb-3">
                    <label for="user.org_id">organisation</label>
                    <Field class="form-control" id="user.org_id" name="user.org_id" v-model="user.org_id"
                        :class="{ 'is-invalid': errors['user.org_id'] }">
                    </Field>
                    <div class=" invalid-feedback">{{ errors['user.org_id'] }}</div>
                </div>
                <div class="mb-3">
                    <label for="user.role_id">role</label>
                    <Field class="form-control" id="user.role_id" name="user.role_id" v-model="user.role_id"
                        :class="{ 'is-invalid': errors['user.role_id'] }">
                    </Field>
                    <div class=" invalid-feedback">{{ errors['user.role_id'] }}</div>
                </div>
                <div v-if="errors.apiError" class="w-100 alert alert-danger mt-3 mb-3">
                    {{ errors.apiError }}
                </div>
                <button type="submit" class="btn btn-primary" :class="{ 'disabled': status.creating }">
                    <span v-if="status.creating">
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    </span>
                    <span v-if="!status.creating">Create</span>
                </button>
            </Form>
        </div>
    </div>
</template>