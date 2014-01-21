/** John Resig pseudo-Class - 
 * Modification by Regis FLORET to implement signals/slots
 */
(function(){
    var a=false,
        b=/xyz/.test(function(){xyz})?/\binherit\b/:/.*/;
    
    this.Class=function(){};
    
    Class.extend = function(args){
        var f=this.prototype;
        a=true;
        var self = new this();
        a=false;
        
        for(var el in args){
            self[el] = typeof args[el]=="function" && typeof f[el]=="function" && b.test(args[el]) ? (function(h , i){
                return function(){
                    var k = this.inherit;
                    this.inherit = f[h];
                    var j = i.apply(this,arguments);
                    this.inherit = k;
                    return j;
                }
            })(el, args[el]) : args[el];
        }
        
        function klass(){
            if(!a && this.init) {
                this.init.apply(this,arguments);
            }
        }
        
        klass.prototype = self;
        klass.prototype.constructor=klass;
        klass.extend = arguments.callee;
        
        klass.prototype.es = [];
        
        klass.prototype.connect = function(e,f) {
            for(var i=0; i<this.es.length;i++) {
                if (this.es[i].en == e && this.es[i].fu == f) {
                    return klass;
                }
            }
            this.es.push({en:e,fu:f});
            return this;
        };
        
        klass.prototype.on = klass.prototype.connect;
        
        klass.prototype.disconnect = function(e) {
            var r=[];
            
            for(var i=0;i<this.es.length;i++) {
                if (this.es[i].en==e) {
                    r.push(i);
                }
            }
            
            for(var i=0;i<r.length;i++){
                this.es.splice(i,1)
            }
            return this;
        };
        klass.prototype.off = klass.prototype.disconnect;
        
        klass.prototype.disconnectAll=function(){
            this.es=[];
            return this;
        };
        
        klass.prototype.emit=function(e, a){
            for(var i=0;i<this.es.length;i++){
                if (this.es[i].en==e){
                    this.es[i].fu(a);
                }
            }
            return this;
        };
        
        klass.prototype.reemit=function(evt, dest) {
            return this.on(evt, function(data) {dest.emit(evt, data)});
        }
        
        return klass;
    }
    
})();

