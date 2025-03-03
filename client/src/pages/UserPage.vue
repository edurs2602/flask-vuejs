<template>
    <v-container>
      <v-btn @click="goBackToList" color="primary">Back to List</v-btn>
  
      <v-data-table :headers="headers" :items="[user]" item-key="_id">
        <template v-slot:item.username="{ item }">
          <v-btn text :to="'/user/' + item._id">{{ item.username }}</v-btn>
        </template>
  
        <template v-slot:item.roles="{ item }">
          <span>{{ item.roles.join(', ') }}</span>
        </template>
  
        <template v-slot:item.timezone="{ item }">
          <span>{{ item.preferences.timezone }}</span>
        </template>
  
        <template v-slot:item.active="{ item }">
          <span>{{ item.active ? 'Yes' : 'No' }}</span>
        </template>
  
        <template v-slot:item.created_ts="{ item }">
          <span>{{ formatDate(item.created_ts) }}</span>
        </template>
  
        <template v-slot:item.actions="{ item }">
          <v-btn @click="openEditDialog(item)">Edit</v-btn>
          <v-btn @click="deleteUser(item)">Delete</v-btn>
        </template>
      </v-data-table>
  
      <v-dialog v-model="editDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Edit User</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="editForm" v-model="isEdit" v-if="selectedUser">
              <v-text-field
                v-model="selectedUser.username"
                label="Username"
                required
                :rules="[v => !!v || 'Username is required']"
              ></v-text-field>
  
              <v-text-field
                v-model="selectedUser.rolesString"
                label="Roles (comma separated)"
                required
                :rules="[v => !!v || 'Roles are required']"
              ></v-text-field>
  
              <v-text-field
                v-model="selectedUser.preferences.timezone"
                label="Timezone"
                required
                :rules="[v => !!v || 'Timezone is required']"
              ></v-text-field>
  
              <v-text-field
                v-model="selectedUser.password"
                label="Password"
                type="password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="closeEditDialog">Cancel</v-btn>
            <v-btn @click="saveUser" color="primary">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  export default {
    props: {
      user: Object,
    },
    data() {
      return {
        headers: [
          { text: 'Username', value: 'username' },
          { text: 'Roles', value: 'roles' },
          { text: 'Timezone', value: 'timezone' },
          { text: 'Is Active?', value: 'active' },
          { text: 'Created At', value: 'created_ts' },
          { text: 'Actions', value: 'actions', sortable: false },
        ],
        selectedUser: null,
        editDialog: false,
        isEdit: false,
      };
    },
    methods: {
      goBackToList() {
        this.$router.push('/');
      },
  
      openEditDialog(user) {
        this.selectedUser = {
          ...user,
          rolesString: user.roles.join(', '),
        };
        this.isEdit = true;
        this.editDialog = true;
      },
  
      saveUser() {
        const userData = {
          ...this.selectedUser,
          roles: this.selectedUser.rolesString.split(',').map(role => role.trim()),
        };
  
        if (this.$refs.editForm.validate()) {
          const userId = this.selectedUser._id.$oid || this.selectedUser._id;
  
          fetch(`http://localhost:5001/users/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
          })
            .then(() => {
              this.$router.push('/');
            })
            .catch((error) => {
              console.error('Error updating user:', error);
              alert('Error updating user');
            });
        }
      },
  
      closeEditDialog() {
        this.editDialog = false;
        this.selectedUser = null;
      },
  
      deleteUser(user) {
        const confirmDelete = confirm('Are you sure you want to delete this user?');
        if (confirmDelete) {
          const userId = user._id.$oid || user._id;
          fetch(`http://localhost:5001/users/${userId}`, { method: 'DELETE' })
            .then(() => this.$router.push('/'));
        }
      },
  
      formatDate(timestamp) {
        const date = new Date(timestamp * 1000);
        return date.toLocaleString();
      },
    },
  };
  </script>
  