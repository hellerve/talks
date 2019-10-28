(require '[clojure.string :as str])

(defmacro exc [& msgs]
  `(throw (Exception. (str ~@msgs))))

(defmacro fmt [s & args]
  (let [a (dec (count (filter #(not= "" %) (str/split s #"%"))))
        b (count args)]
    (if (= a b)
      `(apply format ~s '~args)
      (exc "arguments to format don’t match (expected " a ", got " b ")"))))

(defmacro todo! [ts & body]
  (let [ts (eval ts)]
    (if (.after ts (java.util.Date. (System/currentTimeMillis)))
      (exc "TODO has passed its due date—it was due on "
           (.toString (java.util.Date. ts)))
      `(do ~@body))))
