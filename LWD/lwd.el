;; references: outline.el, hilit19.el
;;
;; コメントを隠したり表示したりするインターフェイス
;; (テスト版 Fortranのみ対応)
;;                  1999/09/22 押入
;; (ほとんど全面改造平成１１年１０月７日(木)matto)
;; (modfiy flagが立つbug fix.
;;  bufferの最後のコメントが消えないbug fix.  1999/10/13 押入)
;; (GYoumatsu no ichi wo 1 zurashita.)
;;
;;    使い方
;;           まずlwd.elファイルをロードしてlwd-modeを実行する
;;
;;            \C-ch (トグル)
;;           -> 通常表示 -> コメント隠す ->
;;
;;         (コメントを隠している時のみ)
;;            \C-cn
;;              次のコメントを表示
;;            \C-cp
;;              前のコメントを表示(予定)
;;            \C-cu
;;              次のコメントを隠す
;;            \C-ci
;;              前のコメントを隠す(予定)
;;
;;
;;  (推奨)
;;    コメントとプログラムとは同じ行に書かない
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

;;;これらの変数はすべてバッファごとに別個に持つ必要がある。
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
;;  toggleのための関数群
;;
;;
(defun lwd-toggle-mode ()
    (interactive)
      (cond
;;ノーマル
       (lwd-toggle-flag 
	(setq lwd-toggle-flag nil)
	(lwd-show-region (point-min) (point-max)))
;;コメント消える
       (t
	(setq lwd-toggle-flag t)
	(lwd-hide-region (point-min) (point-max)))))

(setq lwd-empty-regexp "[ \t\n\f]*")

(defun lwd-next-comment ()
  "point以降の最初のコメントに移動."
;;  (interactive)
  (if (re-search-forward lwd-comment-start-regexp nil 'move)
      (goto-char (match-beginning 0))))

(defun lwd-next-body ()
  "point以降の最初のボディに移動. この関数はpointがコメントの内部にある時に正しく動作する。"
;;  (interactive)
  (let ((=Last)))
  (if lwd-comment-end-regexp
      (if (re-search-forward lwd-comment-end-regexp nil 'move)
	  (progn
	    ;;空白をスキップする。
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
    ;;行の終わりまでのコメントの場合
    (progn
      (while (progn
	       (end-of-line)
	       ;(forward-char +1)
	       (setq =Last (point))
	       (re-search-forward lwd-empty-regexp nil 'move)
	       (and (not (eobp)) (looking-at lwd-comment-start-regexp))))
      (goto-char =Last))))

(defun lwd-hide-region (start end)
  "指定された領域のなかの、コメント部分を縮小する。"
;;はじめからstartがcomment領域内だった場合は？
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      (narrow-to-region start end)
      ;;文頭へ
      (goto-char (point-min))
      ;;次のコメントへ移動してマーク
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
  "コメント部分を縮小する。"
  (interactive)
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      ;;次のコメントへ移動してマーク
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
  "コメント部分を表示する。"
  (interactive)
  (let ((lwd-head-of-comment)
	(=Mod)))
  (setq =Mod (buffer-modified-p))
  (save-excursion
    (save-restriction
      ;;次のコメントへ移動してマーク
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


