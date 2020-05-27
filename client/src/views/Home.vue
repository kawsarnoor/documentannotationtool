<template>
  <div class="home">
    <div class="row home-row" >
      <div class="col-sm-2" id='progress'>
        <Progress  :numbers="numbers" @number-added="numbers = $event"/>
      </div>
      <div class="col-sm-10">
        <Document msg="Medical Text Classification Annotation Tool"/>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Progress from '@/components/Progress.vue';
import Document from '@/components/Document.vue';

export default {
  name: 'Home',
  components: {
    Progress,
    Document,
  },
  data() {
    return {
      numbers: 0,
    };
  },
};
</script>

<style scoped>
.home {
  margin: 40px 0px 0px 0px;
}

.home-row {
  height: 100%;
}

#progress{
  height: 100%;
}

</style>
