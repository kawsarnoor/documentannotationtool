<template>
<!-- eslint-disable max-len -->
    <div class="container" id="progress">
        <img alt="Vue logo" src="../assets/uclh.png" style="max-width: 60%">
        <div class="card text-center">
            <div class="card-header">
                History
            </div>
            <!-- <div class="card-body overflowAuto">
                <ol>
                    <li v-for="indx in history" :key="indx">{{ indx }}</li>
                </ol>

            </div> -->
            <div class="list-group list-group-flush">

                <template v-for="(docindx, i) in history">
                    <div class="btn-group" :key="docindx" role="group" aria-label="Basic example">
                        <div class="input-group-prepend">
                            <div class="input-group-text" id="btnGroupAddon">{{ i }}</div>
                        </div>
                        <button v-if="i==currentidx" :key="docindx"  type="button" class="list-group-item list-group-item-action active" @click="goToDocument(i)">Document {{ docindx }}</button>
                        <button v-else type="button" :key="docindx"  class="list-group-item list-group-item-action" @click="goToDocument(i)">Document {{ docindx }}</button>
                    </div>
                </template>
            </div>
        </div>
        <div>
            <button class="btn btn-primary" type="button" style="margin-right: 15px; margin-top: 10px;" @click="prev()">Prev</button>
            <button class="btn btn-primary" type="button" style="margin-left: 15px; margin-top: 10px;" @click="next()">Next</button>
        </div>
    </div>
</template>

<script>
/*eslint-disable*/
import axios from 'axios';
import { EventBus } from "../main.js";

export default {
  name: 'Progess',
  props: {
    numbers: Number,
  },
  data() {
      return {
        currentidx: Number,
        history: [],
      };
  },
  methods: {
    next() {
      const path = 'http://localhost:5001/getHistory';
      axios.get(path)
        .then((res) => {
            this.history = res.data.history;
            
            if ((this.history.length - 1) === this.currentidx) {
                // Need to sample
                var path = 'http://localhost:5001/sampleNewDocument';
                axios.get(path, {})
                    .then(() => {
                        this.currentidx = this.currentidx + 1;
                        EventBus.$emit("number-added", -1);
                    })
                    .catch((error) => {
                    console.error(error);
                });
                var path = 'http://localhost:5001/getHistory';
                axios.get(path)
                    .then((res) => {
                        this.history = res.data.history;
                    })
                    .catch((error) => {
                    console.error(error);
                });                  
            }
            else{
                this.currentidx = this.currentidx + 1;
                EventBus.$emit("number-added", this.currentidx);
            } 
        })
        .catch((error) => {
          console.error(error);
      });  
    },

    prev() {
      const path = 'http://localhost:5001/getHistory';
      axios.get(path)
        .then((res) => {
            this.history = res.data.history;
            
            if (this.currentidx === 0) {
                this.currentidx = 0;
                EventBus.$emit("number-added", 0);
            }
            else{
                this.currentidx = this.currentidx -1 ;
                EventBus.$emit("number-added", this.currentidx);
            }
        })
        .catch((error) => {
          console.error(error);
      });  
    },
    goToDocument(i) {
        this.currentidx = i;
        EventBus.$emit("number-added", i);
    }
  },
  created() {
    this.currentidx = 0;
    const path = 'http://localhost:5001/getHistory';
    axios.get(path)
    .then((res) => {
        this.history = res.data.history;
    })
    .catch((error) => {
        console.error(error);
    });  
  }
};
</script>

<style scoped>

#progress{
    background-color: white;
    padding: 0px 0px;
}
.overflowAuto {
  overflow-x: hidden;
  overflow-y: auto;
  height: calc(100vh - 600px);
}

.list-group{
    max-height: 500px;
    margin-bottom: 10px;
    overflow:scroll;
    -webkit-overflow-scrolling: touch;
}
</style>
