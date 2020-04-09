class Model {
    constructor(){
      this._data = {};
    }
  
    add(key, value){
      this._data[key] = value;
    }
  
    get(key){
      return this._data[key];
    }
    remove(key){
        delete this._data[key];
    }
}
  
const model = new Model();
Object.freeze(model);

module.exports = model;