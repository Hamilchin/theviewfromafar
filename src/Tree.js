// PostList.js
import React, { Component } from 'react';

class Tree extends Component {
    render() {
      return (
        <div className="tree">
          <pre>
            {`                                                           .
                                                .         ;
                   .              .              ;%     ;;   
                     ,           ,                :;%  %;   
                      :         ;               [`}
            <a href="#philosophy" onClick={() => this.props.onSelectCategory('philosophy')}>philosophy</a>
            {`]  .,   
             ,.        %;     %;            ;        %;'    ,;
               ;       ;%;  %%;        ,     %;    ;%;    ,%'
                %;       %;%;      ,  ;       %;  ;%;   ,%;' 
                 ;%;   [`}
            <a href="#poetry" onClick={() => this.props.onSelectCategory('writings')}>writings</a>
            {`]   ;%;        % ;%;  ,%;'
                  \`%;.     ;%;     %;'         \`%;%;.%;'
                   \`:%;.    ;%%. %@;        %; ;@%;%'
                      \`:%;.  :;&#%;          %;@%;'
                        \`@%:.  :;%.         ;@@%;'   
                          \`@%.  \`;@%.      ;@@%;         
                            \`@%%. \`@%%    ;@@%;        
                              ;@%. :@%%  %@@%;       
                                %@&)%%%&(%%:;     
                                  #@%%%%%:;;
                                  %#@@%%::;
                                  %#@@o%:;;  . '         
                                  %#@@o%;:(.,'         
                              \`.. %@@(`}<a href="#about" onClick={() => this.props.onSelectCategory('about')}>o</a>{`)::;         
                                 \`)#@@o%::;         
                                  %#@@o%::;        
                                 .%#@@@%::;         
                                 ;%#@@@%::;.          
                                ;%#@@@%%:;;;. 
                            ...;%#@@@@%%:;;;;...                            `}
          </pre>
        </div>
      );
    }
  }
  
export default Tree;
