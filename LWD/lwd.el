;; references: outline.el, hilit19.el
;;
;; $B%3%a%s%H$r1#$7$?$jI=<($7$?$j$9$k%$%s%?!<%U%'%$%9(B
;; ($B%F%9%HHG(B Fortran$B$N$_BP1~(B)
;;                  1999/09/22 $B2!F~(B
;; ($B$[$H$s$IA4LL2~B$J?@.#1#1G/#1#07n#7F|(B($BLZ(B)matto)
;; (modfiy flag$B$,N)$D(Bbug fix.
;;  buffer$B$N:G8e$N%3%a%s%H$,>C$($J$$(Bbug fix.  1999/10/13 $B2!F~(B)
;; (GYoumatsu no ichi wo 1 zurashita.)
;;
;;    $B;H$$J}(B
;;           $B$^$:(Blwd.el$B%U%!%$%k$r%m!<%I$7$F(Blwd-mode$B$r<B9T$9$k(B
;;
;;            \C-ch ($B%H%0%k(B)
;;           -> $BDL>oI=<((B -> $B%3%a%s%H1#$9(B ->
;;
;;         ($B%3%a%s%H$r1#$7$F$$$k;~$N$_(B)
;;            \C-cn
;;              $B<!$N%3%a%s%H$rI=<((B
;;            \C-cp
;;              $BA0$N%3%a%s%H$rI=<((B($BM=Dj(B)
;;            \C-cu
;;              $B<!$N%3%a%s%H$r1#$9(B
;;            \C-ci
;;              $BA0$N%3%a%s%H$r1#$9(B($BM=Dj(B)
;;
;;
;;  ($B?d>)(B)
;;    $B%3%a%s%H$H%W%m%0%i%`$H$OF1$89T$K=q$+$J$$(B
;;

(defun lwd-mode ()
    (interactive)
;;matto hacks
    (setq selective-display t)
    (setq selective-display-ellipses t)
    (make-local-variable 'line-move-ignore-invisible)
    (setq line-move-ignore-invisible t)
    (setq buffer-invisibility-spec '((t . t)))

    (local-set-key "\C-ch" 'lwd-toggle-mode)
    (local-set-key "\C-cn" 'lwd-show-next-comment)
    (local-set-key "\C-cu" 'lwd-hide-next-comment)
;;for test
;;    (local-set-key "\C-ct" 'lwd-next-comment)
;;    (local-set-key "\C-cy" 'lwd-next-body)

;;;$B$3$l$i$NJQ?t$O$9$Y$F%P%C%U%!$4$H$KJL8D$K;}$DI,MW$,$"$k!#(B
    (make-local-variable 'lwd-toggle-flag)
    (setq lwd-toggle-flag nil)
    (make-local-variable 'lwd-comment-start-regexp)
    (make-local-variable 'lwd-comment-end-regexp)
    (if (equal mode-name "C")
	(progn
	  (setq lwd-comment-start-regexp "/\\*")
	  (setq lwd-comment-end-regexp "\\*/"))
      (if (equal mode-name "Fortran")
	  (progn
	    (setq lwd-comment-start-regexp "^[Cc].*$")
	    (setq lwd-comment-end-regexp nil))
	(if (equal mode-name "F90")
	    (progn
	      (setq lwd-comment-start-regexp "!.*$")
	      (setq lwd-comment-end-regexp nil)
	      )))))

;;
;;
;;  toggle$B$N$?$a$N4X?t72(B
;;
;;
(defun lwd-toggle-mode ()
    (interactive)
      (cond
;;$B%N!<%^%k(B
       (lwd-toggle-flag 
	(setq lwd-toggle-flag nil)
	(lwd-show-region (point-min) (point-max)))
;;$B%3%a%s%H>C$($k(B
       (t
	(setq lwd-toggle-flag t)
	(lwd-hide-region (point-min) (point-max)))))

(setq lwd-empty-regexp "[ \t\n\f]*")

(defun lwd-next-comment ()
  "point$B0J9_$N:G=i$N%3%a%s%H$K0\F0(B."
;;  (interactive)
  (if (re-search-forward lwd-comment-start-regexp nil 'move)
      (goto-char (match-beginning 0))))

(defun lwd-next-body ()
  "point$B0J9_$N:G=i$N%\%G%#$K0\F0(B. $B$3$N4X?t$O(Bpoint$B$,%3%a%s%H$NFbIt$K$"$k;~$K@5$7$/F0:n$9$k!#(B"
;;  (interactive)
  (let ((=Last)))
  (if lwd-comment-end-regexp
      (if (re-search-forward lwd-comment-end-regexp nil 'move)
	  (progn
	    ;;$B6uGr$r%9%-%C%W$9$k!#(B
	    (setq =Last (point))
	    (re-search-forward lwd-empty-regexp nil 'move)
	    (while (and (not (eobp))
			(looking-at lwd-comment-start-regexp))
	      (if (re-search-forward lwd-comment-end-regexp nil 'move)
		  (progn 
		    (setq =Last (point))
		    (re-search-forward lwd-empty-regexp nil 'move)
		    )))
	    (goto-char =Last)))
    ;;$B9T$N=*$o$j$^$G$N%3%a%s%H$N>l9g(B
    (progn
      (while (progn
	       (end-of-line)
	       ;(forward-char +1)
	       (setq =Last (point))
	       (re-search-forward lwd-empty-regexp nil 'move)
	       (and (not (eobp)) (looking-at lwd-comment-start-regexp))))
      (goto-char =Last))))

(defun lwd-hide-region (start end)
  "$B;XDj$5$l$?NN0h$N$J$+$N!"%3%a%s%HItJ,$r=L>.$9$k!#(B"
;;$B$O$8$a$+$i(Bstart$B$,(Bcomment$BNN0hFb$@$C$?>l9g$O!)(B
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      (narrow-to-region start end)
      ;;$BJ8F,$X(B
      (goto-char (point-min))
      ;;$B<!$N%3%a%s%H$X0\F0$7$F%^!<%/(B
      ;;osiire hack "while condition"
      (while (and (not (eobp)) (lwd-next-comment))
	(progn
	  (setq lwd-head-of-comment (point))
	  (lwd-next-body)
	  (setq lwd-end-of-comment (point))
	  (put-text-property lwd-head-of-comment 
			     lwd-end-of-comment 'invisible t)
		))))
  (set-buffer-modified-p =Mod))

(defun lwd-show-region (start end)
  (interactive)
  (let ((=Mod)))
  (setq =Mod (buffer-modified-p))
  (put-text-property start end 'invisible nil)
  (set-buffer-modified-p =Mod))

(defun lwd-hide-next-comment ()
  "$B%3%a%s%HItJ,$r=L>.$9$k!#(B"
  (interactive)
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      ;;$B<!$N%3%a%s%H$X0\F0$7$F%^!<%/(B
      ;;osiire hack
      (if (lwd-next-comment)
	  (progn
	    (setq lwd-head-of-comment (point))
	    (lwd-next-body)
	    (setq lwd-end-of-comment (point))
	    (put-text-property lwd-head-of-comment 
			       lwd-end-of-comment 'invisible t)
	    ))))
  (set-buffer-modified-p =Mod)
  (goto-char lwd-end-of-comment))

(defun lwd-show-next-comment ()
  "$B%3%a%s%HItJ,$rI=<($9$k!#(B"
  (interactive)
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      ;;$B<!$N%3%a%s%H$X0\F0$7$F%^!<%/(B
      ;;osiire hack
      (if (lwd-next-comment)
	  (progn
	    (setq lwd-head-of-comment (point))
	    (lwd-next-body)
	    (setq lwd-end-of-comment (point))
	    (put-text-property lwd-head-of-comment
			       lwd-end-of-comment 'invisible nil)
	    ))))
  (set-buffer-modified-p =Mod)
  (goto-char lwd-end-of-comment))


