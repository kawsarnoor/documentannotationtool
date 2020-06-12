<template>
<!-- eslint-disable max-len -->
  <div class="document">
    <div class="card text-center">
      <div class="card-header">
        Document {{ labels.id }}
      </div>
      <div class="card-body overflowAuto">
        <h5 class="card-title">What Happened</h5>
        <p class="card-text">
          <a v-for="(word, index) in labels.whathappened" :key="index">
            <span v-if="checkSpanStatus(index)" :id="'sp_' + (index)" style="backgroundColor: #00FFFF;">{{word}}</span>
            <span v-else :id="'sp_' + (index)">{{word}}</span>
          </a>
        </p>
        <h5 class="card-title">Actions Preventing Reoccurence</h5>
        <p class="card-text">
          <a v-for="(word, index) in labels.actionspreventing" :key="index">
            <span v-if="checkSpanStatus(index + labels.whathappened.length)" :id="'sp_' + (index + labels.whathappened.length)" style="backgroundColor: #00FFFF;">{{word}}</span>
            <span v-else :id="'sp_' + (index + labels.whathappened.length)">{{word}}</span>
          </a>
        </p>
      </div>
    </div>
    <div>
      <div class="category">
        <h5>Themes</h5>
        <div class="row">
          <div class="col-10">
            <div class="btn-group" role="group" v-for="(value, label) in labels.themes" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'themes', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'themes', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'themes', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'themes', labels.id)">&#10078;</button>
            </div>
          </div>
          <div class="col-2">
            <form class="form-inline">
              <input type="text" id="themes-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('themes-new')">
            </form>
          </div>
        </div>
      </div>
      <div class="category">
        <h5>Outcomes</h5>
        <div class="row">
          <div class="col-10">
            <div class="btn-group" role="group" v-for="(value, label) in labels.outcomes" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'outcomes', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'outcomes', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'outcomes', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'outcomes', labels.id)">&#10078;</button>
            </div>
          </div>
          <div class="col-2">
            <form class="form-inline">
              <input type="text" id="outcomes-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('outcomes-new')">
            </form>
          </div>
        </div>
      </div>
      <div class="category">
        <h5>Barriers</h5>
        <div class="row">
          <div class="col-10">
            <div class="btn-group" role="group" v-for="(value, label) in labels.barriers" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'barriers', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'barriers', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'barriers', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'barriers', labels.id)">&#10078;</button>
            </div>
          </div>
          <div class="col-2">
            <form class="form-inline">
              <input type="text" id="barriers-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('barriers-new')">
            </form>
          </div>
        </div>
      </div>
      <div class="category">
        <h5>Stage of Care</h5>
          <div class="row">
            <div class="col-10">
              <div class="btn-group" role="group" v-for="(value, label) in labels.stageofcare" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'stageofcare', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'stageofcare', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'stageofcare', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'stageofcare', labels.id)">&#10078;</button>
              </div>
            </div>
            <div class="col-2">
            <form class="form-inline">
              <input type="text" id="stageofcare-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('stageofcare-new')">
            </form>
            </div>
          </div>
      </div>
      <div class="category">
        <h5>Error</h5>
          <div class="row">
            <div class="col-10">
              <div class="btn-group" role="group" v-for="(value, label) in labels.error" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'error', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'error', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'error', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'error', labels.id)">&#10078;</button>
              </div>
            </div>
            <div class="col-2">
            <form class="form-inline">
              <input type="text" id="error-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('error-new')">
            </form>
            </div>
          </div>
      </div>
      <div class="category">
        <h5>Known Allergy</h5>
        <div class="row">
          <div class="col-10">
            <div class="btn-group" role="group" v-for="(value, label) in labels.knownallergy" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'knownallergy', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'knownallergy', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'knownallergy', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'knownallergy', labels.id)">&#10078;</button>
            </div>
          </div>
          <div class="col-2">
            <form class="form-inline">
              <input type="text" id="knownallergy-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('knownallergy-new')">
            </form>
          </div>
        </div>
      </div>
      <div class="category">
        <h5>Certainty / Severity of Allergy</h5>
        <div class="row">
          <div class="col-10">
            <div class="btn-group" role="group" v-for="(value, label) in labels.certaintyallergy" :key="label">
                  <button v-if="value == false" class="btn btn-secondary" type="button" @click="changeValue(label, 'certaintyallergy', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-primary" type="button" @click="showSpans(label, 'certaintyallergy', labels.id)">{{label}} </button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="changeValue(label, 'certaintyallergy', labels.id)">&#10008;</button>
                  <button v-if="value == true" class="btn btn-warning" type="button" @click="linkTexttoLabel(label, 'certaintyallergy', labels.id)">&#10078;</button>
            </div>
          </div>
          <div class="col-2">
            <form class="form-inline">
              <input type="text" id="certaintyallergy-new" class="form-control search" placeholder="new label" @keyup.enter="addlabel('certaintyallergy-new')">
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/*eslint-disable*/

import axios from 'axios';
import rangy from 'rangy';
import $ from 'jquery';
import { EventBus } from "../main.js";

export default {
  name: 'Document',
  props: {
    msg: String,
  },
  data() {
    return {
      labels: [],
      spans: {},
      spanvalues: [],
      numbers: [1, 2, 3],
      currentidx: Number,
      root_api: process.env.VUE_APP_URL,
    };
  },
  methods: {
    getnextdocument(newIdx) {
      const path = 'http://' + this.root_api + ':5001/getDocumentviaIndex';
      axios.post(path, {newIdx})
        .then((res) => {
          console.log(res.data.labels);
          this.labels = res.data.labels;
          this.spans = res.data.spans;
          this.spanvalues = res.data.span_values;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    linkTexttoLabel(label, category, id) {
      const sel = rangy.getSelection();
      const ids = [];
      for (let r = 0, range, spans; r < sel.rangeCount; ++r) {
          range = sel.getRangeAt(r);
          if (range.startContainer == range.endContainer && range.startContainer.nodeType == 3) {
              range = range.cloneRange();
              range.selectNode(range.startContainer.parentNode);
          }
          spans = range.getNodes([1], function(node) {
              return node.nodeName.toLowerCase() == "span";
          });
          for (let i = 0, len = spans.length; i < len; ++i) {
              ids.push(spans[i].id);
          }
      }

      this.spans[category][label] = this.spans[category][label].concat(ids);
      const path = 'http://' + this.root_api + ':5001/updateSpans';
      let newspans = this.spans[category][label];
      
      axios.post(path, {category, label, newspans, id })
        .then(() => {
          this.getnextdocument(this.currentidx);
        })
        .catch((error) => {
          console.error(error);
      });
    },
    changeValue(label, category, id) {
      console.log(label);
      const path = 'http://' + this.root_api + ':5001/changelabel';
      axios.post(path, { label, category, id })
        .then((res) => {
          if(res.data.new_value){
            this.linkTexttoLabel(label, category, id);
          }
          else{
            this.getnextdocument(this.currentidx);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    checkSpanStatus(index) {
      var span = 'sp_' + index;
      return this.spanvalues.includes(span)
    },
    addlabel: function(id) {
      var newlabel = $('#'+ id).val();
      var category = id.split("-")[0];
      const path = 'http://' + this.root_api + ':5001/addlabel';

      axios.post(path, {category, newlabel})
        .then(() => {
          this.getnextdocument(this.currentidx );
          $('#'+ id).val('');
        })
        .catch((error) => {
          console.error(error);
        });      
     },
  },
  created() {
    this.getnextdocument(0);

    EventBus.$on("number-added", newIdx => {
      this.currentidx = newIdx;
      this.getnextdocument(newIdx);
    });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input {
  margin: 3px;
}
h3 {
  margin: 0px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.category {
  text-align: left;
  margin-top: 15px;
}
.overflowAuto {
  overflow-x: hidden;
  overflow-y: auto;
  height: calc(100vh - 700px);
}
.document {
  margin: 15px;
}
.btn-group {
  margin: 5px;
}
div.boxwrap div {
  float: left;
}
div.boxwrap div:hover {
  background-color: aqua;
  cursor: pointer;
}
div.boxwrap div h5 {
  text-align: center;
}
</style>
