<template>
    <v-data-table :headers="headers" :items="users" item-key="_id">
      <template v-slot:item.username="{ item }">
        <v-btn text :to="'/user/' + item._id.$oid">{{ item.username }}</v-btn>
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
        <v-btn @click="editUser(item)">Edit</v-btn>
        <v-btn @click="deleteUser(item)">Delete</v-btn>
      </template>
    </v-data-table>
</template>

<script>
export default {
  props: ['users'],
  data() {
    return {
      headers: [
        { text: 'Username', value: 'username' },
        { text: 'Roles', value: 'roles' },
        { text: 'Timezone', value: 'timezone' },
        { text: 'Is Active?', value: 'active' },
        { text: 'Last Updated At', value: 'lastUpdatedAt', sortable: false },
        { text: 'Created At', value: 'created_ts' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    editUser(user) {
      const userId = user._id.$oid;
      if (userId) {
        this.$emit('edit', user);
      } else {
        console.error('User ID not found');
      }
    },
  
    deleteUser(user) {
      const userId = user._id.$oid;
      if (userId) {
        const confirmDelete = confirm('Are you sure you want to delete this user?');
        if (confirmDelete) {
          this.$emit('delete', user);
        }
      } else {
        console.error('User ID not found');
      }
    },
  
    formatDate(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    }
  }
}
</script>
