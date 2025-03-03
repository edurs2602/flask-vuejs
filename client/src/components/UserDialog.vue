<template>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ isEdit ? 'Edit User' : 'Create User' }}</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="user.username" label="Username" required></v-text-field>
            <v-text-field v-model="user.roles" label="Roles" required></v-text-field>
            <v-text-field v-model="user.timezone" label="Timezone" required></v-text-field>
            <v-checkbox v-model="user.isActive" label="Is Active?"></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeDialog">Cancel</v-btn>
          <v-btn @click="saveUser">{{ isEdit ? 'Save' : 'Create' }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    props: ['user', 'isEdit'],
    data() {
      return {
        dialog: false
      }
    },
    methods: {
      openDialog() {
        this.dialog = true;
      },
      closeDialog() {
        this.dialog = false;
      },
      saveUser() {
        this.$emit('save', this.user);
        this.closeDialog();
      }
    },
    watch: {
      user: function() {
        if (this.user) {
          this.openDialog();
        }
      }
    }
  }
  </script>
  