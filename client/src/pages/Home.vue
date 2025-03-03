<template>
    <v-container>
      <v-btn @click="openCreateDialog">Create User</v-btn>
  
      <UserTable :users="users" @edit="openEditDialog" @delete="deleteUser" />
      
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">{{ isEdit ? 'Edit User' : 'Create User' }}</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" :model="isEdit">
              <v-text-field
                v-model="userToEdit.username"
                label="Username"
                required
                :rules="[v => !!v || 'Username is required']"
              ></v-text-field>
              <v-text-field
                v-model="userToEdit.password"
                label="Password"
                type="password"
                required
                :rules="[v => !!v || 'Password is required']"
              ></v-text-field>
              <v-text-field
                v-model="userToEdit.roles"
                label="Roles (comma separated)"
                required
                :rules="[v => !!v || 'Roles are required']"
              ></v-text-field>
              <v-text-field
                v-model="userToEdit.preferences.timezone"
                label="Timezone"
                required
                :rules="[v => !!v || 'Timezone is required']"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="closeDialog">Cancel</v-btn>
            <v-btn @click="saveUser" color="primary">{{ isEdit ? 'Save' : 'Create' }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import UserTable from '@/components/UserTable.vue';
  
  export default {
    components: {
      UserTable,
    },
    data() {
      return {
        users: [],
        userToEdit: null,
        isEdit: false,
        dialog: false,
      };
    },
    created() {
      this.fetchUsers();
    },
    methods: {
      fetchUsers() {
        fetch('http://localhost:5001/users')
          .then(response => response.json())
          .then(data => {
            this.users = data;
          })
          .catch(error => console.error('Error fetching users:', error));
      },
  
      openCreateDialog() {
        this.isEdit = false;
        this.userToEdit = {
          username: '',
          password: '',
          roles: '',
          preferences: {
            timezone: ''
          },
        };
        this.dialog = true;
      },
  
      openEditDialog(user) {
        this.isEdit = true;
        this.userToEdit = { ...user };
        if (this.userToEdit.roles && Array.isArray(this.userToEdit.roles)) {
          this.userToEdit.roles = this.userToEdit.roles.join(', ');
        }
        this.dialog = true;
      },
  
      closeDialog() {
        this.dialog = false;
      },
  
      saveUser() {
        const userData = {
          username: this.userToEdit.username,
          password: this.userToEdit.password,
          roles: this.userToEdit.roles.split(',').map(role => role.trim()),
          preferences: {
            timezone: this.userToEdit.preferences.timezone
          },
          active: true,
          created_ts: Math.floor(Date.now() / 1000)
        };
  
        if (this.$refs.form.validate()) {
          if (this.isEdit) {
            const userId = this.userToEdit._id.$oid;
            fetch(`http://localhost:5001/users/${userId}`, {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(userData)
            })
              .then(() => {
                this.fetchUsers();
                this.closeDialog();
              })
              .catch(error => {
                console.error('Error updating user:', error);
                alert('Error updating user');
              });
          } else {
            fetch('http://localhost:5001/users', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(userData)
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error('Failed to create user');
                }
                return response.json();
              })
              .then(() => {
                this.fetchUsers();
                this.closeDialog();
              })
              .catch(error => {
                console.error('Error creating user:', error);
                alert('Error creating user');
              });
          }
        }
      },
  
      deleteUser(user) {
        const userId = user._id.$oid;
        const confirmDelete = confirm('Are you sure you want to delete this user?');
        if (confirmDelete) {
          fetch(`http://localhost:5001/users/${userId}`, { method: 'DELETE' })
            .then(() => {
              this.users = this.users.filter(u => u._id.$oid !== userId);
            })
            .catch((error) => console.error('Error deleting user:', error));
        }
      }
    }
  };
  </script>
  