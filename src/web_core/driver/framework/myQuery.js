const QUTILS = {
    get: function(selectors) {
        return this.querySelector(selectors);
    },

    getAll: function(selectors) {
        return [...this.querySelectorAll(selectors)];
    },

    /**
     * hides html element from web view
     * @returns same element for method chaining
     */
    hide: function() {
        this.style.display = "none";
        return this;
    },

    /**
     * shows html element in view
     * @returns {UTILS}
     */
    show: function() {
        this.style.display = "";
        return this;
    },

    addTo: function(parent){
        parent.appendChild(this);
        return this;
    },

    addClass: function(...new_classes) {
        this.classList.add(...new_classes);
        return this;
    },

    removeClass: function(...removed_classes) {
        this.classList.remove(...removed_classes);
        return this;
    },

    setId: function(id) {
        this.id = id;
        return this
    }

    /**
     * add event listeners but better
     * @param event_callback_pairs {event: callback}
     * @returns {QUTILS}
     */
    when: function(event_callback_pairs){
        for(let event in event_callback_pairs){
            this.addEventListener(event, event_callback_pairs[event]);
        }

        return this;
    },
};
//HTMLElement.prototype.
// automatically assign above utils to prototype of html element instead of manually assign
for (let util in QUTILS){
    HTMLElement.prototype[util] = QUTILS[util];
}

/*
HTMLElement.prototype.hide = QUTILS.hide;
HTMLElement.prototype.show = QUTILS.show;
HTMLElement.prototype.addTo = QUTILS.addTo;
HTMLElement.prototype.addClass = QUTILS.addClass;
HTMLElement.prototype.removeClass = QUTILS.removeClass;
*/

let Q = {

    /**
     * retrieve an element from the DOM
     * @param selectors css style selectors
     * @returns {*}
     */
    get: function(selectors){
        return document.querySelector(selectors);
    },

    /**
     * retrieve all elements matching selectors from the DOM
     * @param selectors css style selectors
     * @returns {*}
     */
    getAll: function(selectors){
        return [...document.querySelectorAll(selectors)];
    },

    /**
     * get class label element from template div in the DOM
     * @param label the name of a class
     * @returns {Node} a clone of the template in the DOM
     */
    getTemplate: (label) => document.querySelector("#templates ." + label).cloneNode(true),

    // main element in html
    main: null,

    init: function() {
        Q.main = Q.get("#main");
    },
};

const Beti = {
    done: function(id) {
    // Call this function to signal to the hydrater that the page is good to load. The hydrater is responsible for its internal workings.
    const beti_element = document.createElement("div")
    beti_element.setId(id).addTo(Q.get("body"))
    }
}

//"li.text-body-small a.ember-view"