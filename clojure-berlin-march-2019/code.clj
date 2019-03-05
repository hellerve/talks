(defmacro mcomment [& args] nil)
(mcomment
  (+ 40 3)
  (undefined-function)
  (println "nope"))

(defn mtrue [x y] (x))
(defn mfalse [x y] (y))
(defmacro mif [cnd then else] `(~cnd #(~then) #(~else)))
(mif mfalse
  (println "nope")
  (println "yup"))

(defmacro mcond [& args]
  (when args
    `(if ~(first args) ~(second args) ~(cons 'mcond (rest (rest args))))))
(mcond
  (= 1 2) (println "no")
  (= 2 3) (println "still no")
  true (println "yup"))

(defn mcons [h t] #(if % h t))
(defn mcar [l] (l true))
(defn mcdr [l] (l false))
(println (mcar (mcdr (mcons 1 (mcons 2 3)))))

(defn mlist [& args]
  (loop [res nil, args args]
    (if (empty? args)
      res
      (recur (mcons (first args) res) (rest args)))))
(println (mcar (mcdr (mlist 1 2 3))))

(defmacro mlet [args body]
  (if (= (count args) 2)
    `((fn [~(first args)] ~body) ~(second args))
    `((fn [~(first args)] (mlet ~(rest (rest args)) ~body)) ~(second args))))
(println (mlet [x 1 y 2] (+ x y)))
