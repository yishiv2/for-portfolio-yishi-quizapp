import React, { useState } from 'react';

import './Hint.css';

function Hint({ hintIndex, showNextHint, hints}) {
    // hintsがundefinedの場合は空の配列を使用
    console.log(hints,"hints");
    const safeHints = hints || [];
    return (
        <>
            <div className="hint">
                {safeHints.slice(0, hintIndex).map((hint, index) => (
                    <div className="hint-item" key={index}>{hint.replace(/^\d+\.?\s*/, '').replace(/^\s*/, '').replace(/^ヒント:\s*/, '')}</div>
                ))}
            </div>

            {safeHints.length > 0 && (
                <div className="hint-index">
                    <button onClick={showNextHint}>ヒントを表示( {hintIndex} / {safeHints.length})</button>
                </div>
            )}
        </>
    );
}

export default Hint;